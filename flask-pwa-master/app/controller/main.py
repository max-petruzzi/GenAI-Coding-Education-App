from flask import (
    Blueprint, render_template, request, redirect
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

@bp.route('/submit_form', methods=['POST'])
def submit_form():
    question = request.form.get('question-dropdown')
    youtube_link = request.form.get('youtube-link')
    print(question, youtube_link)

    # Perform any necessary processing with the form data
    # ...

    # Redirect to another page after form submission
    return redirect('/')
