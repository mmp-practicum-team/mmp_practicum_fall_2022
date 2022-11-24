from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask import Flask, request, url_for
from flask import render_template, redirect

from flask_wtf.file import FileAllowed
from wtforms import SubmitField, FileField
from wtforms.validators import DataRequired


app = Flask(__name__, template_folder='html')
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['SECRET_KEY'] = 'hello'
Bootstrap(app)


messages = []

class Message:
    header = ''
    text = ''


class FileForm(FlaskForm):
    file_path = FileField('Path', validators=[
        DataRequired('Specify file'),
        FileAllowed(['csv'], 'CSV only!')
    ])
    submit = SubmitField('Open File')


@app.route('/')
@app.route('/index_js')
def get_index():
    return '<html><center><script>document.write("Hello, i`am Flask Server!")</script></center></html>'


@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/fail')
def get_fail():
    raise ValueError('Fail')


@app.route('/messages', methods=['GET', 'POST'])
def prepare_message():
    message = Message()

    if request.method == 'POST':
        message.header, message.text = request.form['header'], request.form['text']
        messages.append(message)

        return redirect(url_for('prepare_message'))

    return render_template('messages.html', messages=messages)


@app.route('/clear_messages', methods=['POST'])
def clear_messages():
    messages.clear()
    return redirect(url_for('prepare_message'))


@app.route('/file', methods=['GET', 'POST'])
def file():
    file_form = FileForm()

    if request.method == 'POST' and file_form.validate_on_submit():
        lines = file_form.file_path.data.stream.readlines()
        print(f'Uploaded {len(lines)} lines')
        return redirect(url_for('file'))

    return render_template('from_form.html', form=file_form)
