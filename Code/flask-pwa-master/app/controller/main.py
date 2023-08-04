from flask import (
    Blueprint, render_template, request, redirect, url_for
)
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api.formatters import TextFormatter
from dotenv import load_dotenv
import os
import openai

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

bp = Blueprint('main', __name__)

@bp.route('/')
def index():
    return render_template('main/index.html',
                           title='Flask-PWA')


@bp.route('/teacher')
def teacher():
    return render_template('main/teacher.html',
                           title='')

@bp.route('/teacher/assignment')
def teacher_assignment():
    return render_template('main/teacher-creat-assignment.html',
                           title='')
@bp.route('/teacher/metrics')
def teacher_metrics():
    return render_template('main/teacher-metrics.html',
                           title='')

@bp.route('/teacher/submissions')
def teacher_submissions():
    return render_template('main/teacher-submissions.html',
                           title='')


@bp.route('/student')
def student():
    return render_template('main/student.html',
                           title='Student')

@bp.route('/studentResults')
def studentResults():
    score = request.args.get('score')
    question = request.args.get('question')
    youtube_url = request.args.get('youtube_url')
    details = request.args.get('details')
    return render_template('main/studentResults.html',
                           title='Score', score=score, question=question, youtube_url=youtube_url, details=details)

# find the first occurence of a number in a string
def find_first_number(s):
    for i, c in enumerate(s):
        if c.isdigit():
            return int(c)
    return -1

@bp.route('/submit_form', methods=['POST'])
def submit_form():
    question = request.form.get('question-dropdown')
    id = request.form.get('youtube-link')
    if question != "2":
        return redirect("/student")
    try:
        transcript = YouTubeTranscriptApi.get_transcript(id)
        formatter = TextFormatter()
        transcript_str = ' '.join(formatter.format_transcript(transcript).split("\n"))
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "I will present the text transcript of a YouTube video where a student is explaining the machine learning topic of decision trees. The student has a diagram of a decision tree with components labeled 1 through 4. The student will identify each of the components. However, the student might not be correct in their identification. Your job is to assess how accurately the student identifies each of the components. You should ignore punctuation and capitalization when deciding whether the student correctly identifies the component. The correct answers are as follows: 1 is a root node, 2 is a branch, 3 is a decision node, and 4 is a leaf node. Your output should only consist of one number which is the number of incorrectly identified components. No other text should be in the output."},
                {"role": "user", "content": f'Transcript: {transcript_str}'}
            ],
            temperature = 0.0,
            max_tokens = 120
        )
        answer = response['choices'][0]['message']['content']
        incorrect = find_first_number(answer)
        response2 = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "I will present the text transcript of a YouTube video where a student is explaining the machine learning topic of decision trees. The student has a diagram of a decision tree with components labeled 1 through 4. The student will identify each of the components. However, the student might not be correct in their identification. Your job is to determine how accurately the student identifies the components. You should ignore punctuation and capitalization when deciding whether the student correctly identifies the component. The correct answers are as follows: 1 is a root node, 2 is a branch, 3 is a decision node, and 4 is a leaf node. Which components were incorrectly identified?"},
                    {"role": "user", "content": f'Transcript: {transcript_str}'}
                ],
                temperature = 0.0,
                max_tokens = 120
        )
        answer2 = response2['choices'][0]['message']['content']


        score = 5 - incorrect

        return redirect(url_for('main.studentResults',
                            question=question,
                            youtube_url=id,
                            details=answer2,
                            score=score))
    except Exception as e:
        print(e)
        return redirect("/student")
