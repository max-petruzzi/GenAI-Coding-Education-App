from flask import (
    Blueprint, render_template, request, redirect
)

bp = Blueprint('main', __name__)


@bp.route('/')
def index():
    return render_template('main/index.html',
                           title='Flask-PWA')

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