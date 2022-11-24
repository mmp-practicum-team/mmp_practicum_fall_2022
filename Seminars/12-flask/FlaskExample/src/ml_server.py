import os
import pickle

from flask_wtf import FlaskForm
from flask_bootstrap import Bootstrap
from flask import Flask, request, url_for
from flask import render_template, redirect

from wtforms.validators import DataRequired
from wtforms import StringField, SubmitField


app = Flask(__name__, template_folder='html')
app.config['BOOTSTRAP_SERVE_LOCAL'] = True
app.config['SECRET_KEY'] = 'hello'
Bootstrap(app)


data_path = './../artifacts'


class TextForm(FlaskForm):
    text = StringField('Text', validators=[DataRequired()])
    submit = SubmitField('Get Result')


class Response(FlaskForm):
    score = StringField('Score', validators=[DataRequired()])
    sentiment = StringField('Sentiment', validators=[DataRequired()])
    submit = SubmitField('Try Again')


def score_text(text):
    try:
        model = pickle.load(open(os.path.join(data_path, "logreg.pkl"), "rb"))
        tfidf = pickle.load(open(os.path.join(data_path, "tf-idf.pkl"), "rb"))

        score = model.predict_proba(tfidf.transform([text]))[0][1]
        sentiment = 'positive' if score > 0.5 else 'negative'
    except Exception as exc:
        app.logger.info('Exception: {0}'.format(exc))
        score, sentiment = 0.0, 'unknown'

    return score, sentiment


@app.route('/result', methods=['GET', 'POST'])
def get_result():
    try:
        response_form = Response()

        if response_form.validate_on_submit():
            return redirect(url_for('get_text_score'))

        score = request.args.get('score')
        sentiment = request.args.get('sentiment')

        response_form.score.data = score
        response_form.sentiment.data = sentiment

        return render_template('from_form.html', form=response_form)
    except Exception as exc:
        app.logger.info('Exception: {0}'.format(exc))


@app.route('/sentiment', methods=['GET', 'POST'])
def get_text_score():
    try:
        text_form = TextForm()

        if text_form.validate_on_submit():
            app.logger.info('On text: {0}'.format(text_form.text.data))
            score, sentiment = score_text(text_form.text.data)
            app.logger.info("Score: {0:.3f}, Sentiment: {1}".format(score, sentiment))
            text_form.text.data = ''
            return redirect(url_for('get_result', score=score, sentiment=sentiment))
        return render_template('from_form.html', form=text_form)
    except Exception as exc:
        app.logger.info('Exception: {0}'.format(exc))


@app.errorhandler(404)
def handle_404(e):
    return redirect(url_for('get_text_score'))
