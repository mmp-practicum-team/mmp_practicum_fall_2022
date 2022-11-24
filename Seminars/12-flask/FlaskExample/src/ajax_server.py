import os
import base64

from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask import Flask, render_template, render_template_string

from wtforms import SubmitField


app = Flask(__name__, template_folder='html')
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['SECRET_KEY'] = 'hello'
Bootstrap(app)


images_path = './../images'
images_paths, current_image_idx = sorted(os.listdir(images_path)), 0


class SlideShowForm(FlaskForm):
    prev_button = SubmitField('Previous image')
    next_button = SubmitField('Next image')


@app.route('/load_image', methods=['POST'])
def load_image(is_static=False):
    global current_image_idx

    form = SlideShowForm()
    if form.validate_on_submit():
        if form.prev_button.data:
            current_image_idx = current_image_idx - 1 if current_image_idx > 0 else len(images_paths) - 1
        if form.next_button.data:
            current_image_idx = current_image_idx + 1 if current_image_idx < len(images_paths) - 1 else 0

    image_path = os.path.join(images_path, images_paths[current_image_idx])
    with open(image_path, 'rb') as image_file:
        image_data = base64.b64encode(image_file.read()).decode()

    return {
        'path': image_path,
        'form': form if is_static else None,
        'src': 'data:image/png;base64, {0}'.format(image_data)
    }


@app.route('/slideshow', methods=['GET', 'POST'])
def get_slideshow():
    global current_image_idx
    try:
        image_data = load_image(is_static=True)
        return render_template('slideshow.html', image_src=image_data['src'], image_path=image_data['path'], form=image_data['form'])
    except Exception as exc:
        app.logger.info('Exception: {0}'.format(exc))


@app.route('/slideshow_ajax')
def get_slideshow_ajax():
    try:
        image_data = load_image(is_static=True)
        return render_template('slideshow_ajax.html', image_src=image_data['src'], image_path=image_data['path'], form=image_data['form'])
    except Exception as exc:
        app.logger.info('Exception: {0}'.format(exc))


@app.route('/')
def get_index():
    return render_template_string(
        """<html><center><ul>
        <li><a href="{{ url_for('get_slideshow') }}">Base slideshow</a></li>
        <li><a href="{{ url_for('get_slideshow_ajax') }}">AJAX slideshow</a></li>
        </ul></center></html>
        """
    )
