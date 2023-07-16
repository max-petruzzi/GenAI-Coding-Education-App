from flask import (
    Blueprint, render_template, request, redirect, url_for
)

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
    return render_template('main/studentResults.html',
                           title='Score', score=score, question=question, youtube_url=youtube_url)

@bp.route('/submit_form', methods=['POST'])
def submit_form():
    question = request.form.get('question-dropdown')
    youtube_url = request.form.get('youtube-link')
    score = 4.5
    print(question, youtube_url, question)

    return redirect(url_for('main.studentResults',
                        question=question,
                        youtube_url=youtube_url,
                        score=score))
