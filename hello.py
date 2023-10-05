from flask import Flask, render_template, session, redirect, url_for, flash
from flask_bootstrap import Bootstrap
from flask_moment import Moment
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from wtforms.validators import Email
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'ECE444-Assignment1'
bootstrap = Bootstrap(app)
moment = Moment(app)

def validate_name(form, field):
    if 'utoronto' not in field.data:
        form.valid = False

class NameForm(FlaskForm):
    valid = True
    name = StringField('What is your name?', validators=[DataRequired()])
    email = StringField('What is your UofT email address?', validators=[DataRequired(), Email(granular_message=True), validate_name])
    submit = SubmitField('Submit')

@app.route('/', methods=['GET', 'POST'])
def index():
    nameForm = NameForm()

    if nameForm.validate_on_submit():
        old_name = session.get('name')
        old_email = session.get('email')
        if old_email is not None and old_email != nameForm.email.data:
            flash('Looks like you have changed your email!')
        if old_name is not None and old_name != nameForm.name.data:
            flash('Looks like you have changed your name!')
        
        session['name'] = nameForm.name.data
        session['email'] = nameForm.email.data
        session['valid'] = nameForm.valid

        return redirect(url_for('index'))

    return render_template('index.html', nameForm=nameForm, name=session.get('name'), email=session.get('email'), valid=session.get('valid'))

@app.route('/user/<name>')
def user(name):
    return render_template('user.html', name=name)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

@app.errorhandler(500)
def internal_server_error(e):
    return render_template('500.html'), 500