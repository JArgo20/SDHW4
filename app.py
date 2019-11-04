from flask import Flask
from flask import render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY']='SuperSecretKey'

class JobForm(FlaskForm):
    company_name = StringField('Company Name:', validators=[DataRequired()])
    job_title = StringField('Job Title:', validators=[DataRequired()])


@app.route('/')
def index():
    return render_template('index.html', pageTitle='Josiahs Job Applications')

@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    form = JobForm()
    if form.validate_on_submit():
        return "<h2> The company applied to is {0} and the job is {1}".format(form.company_name.data, form.job_title.data)
    
    return render_template('add_job.html', form=form, pageTitle='Add a New Job')