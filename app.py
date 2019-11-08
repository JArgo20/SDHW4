from flask import Flask
from flask import render_template, request, redirect, flash, url_for
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
import pymysql
#import secrets
import os

dbuser = os.environ.get('DBUSER')
dbpass = os.environ.get('DBPASS')
dbhost = os.environ.get('DBHOST')
dbname = os.environ.get('DBNAME')

#conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(secrets.dbuser, secrets.dbpass, secrets.dbhost, secrets.dbname)
conn = "mysql+pymysql://{0}:{1}@{2}/{3}".format(dbuser, dbpass, dbhost, dbname)

app = Flask(__name__)
app.config['SECRET_KEY']='SuperSecretKey'
app.config['SQLALCHEMY_DATABASE_URI'] = conn
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class jargo_jobapp(db.Model):
    jobId = db.Column(db.Integer, primary_key=True)
    company_name = db.Column(db.String(255))
    job_title = db.Column(db.String(255))

    def __repr__(self):
        return "jobId: {0} | Company Name: {1} | Job Title: {2}".format(self.id, self.company_name, self.job_title)

class JobForm(FlaskForm):
    company_name = StringField('Company Name:', validators=[DataRequired()])
    job_title = StringField('Job Title:', validators=[DataRequired()])


@app.route('/')
def index():
    all_jobs = jargo_jobapp.query.all()
    return render_template('index.html', jobs=all_jobs, pageTitle='Josiahs Job Applications')

@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    form = JobForm()
    #if form.validate_on_submit():
    if request.method == 'POST':
        job = jargo_jobapp(company_name=form.company_name.data, job_title=form.job_title.data)
        db.session.add(job)
        db.session.commit()
        return redirect('/')
    
    return render_template('add_job.html', form=form, pageTitle='Add a New Job')

@app.route('/job/<int:jobId>', methods=['GET','POST'])
def job(jobId):
    job = jargo_jobapp.query.get_or_404(jobId)
    return render_template('job.html', form=job, pageTitle='Job Information')

@app.route('/job/<int:jobId>/update', methods=['GET','POST'])
def update_job(jobId):
    job = jargo_jobapp.query.get_or_404(jobId)
    form = JobForm()
    if form.validate_on_submit():
        job.company_name = form.company_name.data
        job.job_title = form.job_title.data
        db.session.commit()
        flash('Job information has been updated.')
        return redirect(url_for('job', jobId=job.jobId))
    form.company_name.data = job.company_name
    form.job_title.data = job.job_title
    return render_template('add_job.html', form=form, pageTitle='Update Post',
                            legend="Update A job")

@app.route('/friend/<int:jobId>/delete', methods=['POST'])
def delete_job(jobId):
    if request.method == 'POST': 
        job = jargo_jobapp.query.get_or_404(jobId)
        db.session.delete(job)
        db.session.commit()
        flash('Job was successfully deleted!')
        return redirect("/")
    else: 
        return redirect("/")