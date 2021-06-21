import os

from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
from datetime import date, datetime
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from wtforms.fields import DateField
from flask_sqlalchemy import SQLAlchemy
import json
from GoogleNews import GoogleNews
googlenews = GoogleNews(period='7d',lang='en')
weekdays = ['MONDAY','TUESDAY','WEDNESDAY','THURSDAY','FRIDAY','SATURDAY','SUNDAY']

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "diary.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)
bootstrap=Bootstrap(app)
datepicker(app)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY

class Entry(db.Model):
    date = db.Column(db.String(), unique=True, nullable=False, primary_key=True)
    headline =  db.Column(db.String())
    goals = db.Column(db.Text())
    notes = db.Column(db.Text())
    grateful = db.Column(db.Text())

    def __repr__(self):
        return "<Title: {}>".format(self.goals)

class EntryForm(FlaskForm):
    edate = DateField('Date',format='%Y-%m-%d', id='datepicker', validators=[DataRequired()], default = date.today)
    grateful = TextAreaField('Grateful',render_kw={"class": "h6 mb-0 font-weight-bold text-gray-800 w-100","contenteditable":"true","aria-multiline":"true"})
    headline = StringField('Headline', render_kw={"class": "h6 mb-0 font-weight-bold text-gray-800 w-100"})
    goals = TextAreaField('Goals',render_kw={"class": "h6 mb-0 font-weight-bold text-gray-800 w-100","contenteditable":"true","aria-multiline":"true"})
    notes = TextAreaField('Notes',render_kw={"class": "h6 mb-0 font-weight-bold text-gray-800 w-100","contenteditable":"true","aria-multiline":"true"})
    submit = SubmitField('Save...')

@app.route("/", methods=["GET", "POST"])
def home():
    form = EntryForm()
    googlenews.search('personal improvement')
    news = googlenews.results()
    if form.validate_on_submit():
        entry = Entry.query.filter_by(date=datetime.strptime(request.form.get("edate"), '%Y-%m-%d').date()).first()
        weekday = datetime.strptime(request.form.get("edate"), '%Y-%m-%d').date().weekday()
        if entry == None:
            entry = Entry(goals=request.form.get("goals"),date=datetime.strptime(request.form.get("edate"), '%Y-%m-%d').date(),notes=request.form.get("notes"),grateful=request.form.get("grateful"),headline=request.form.get("headline") )
            db.session.add(entry)
        else:
            entry.headline = request.form.get("headline")
            entry.notes=request.form.get("notes")
            entry.goals = request.form.get("goals")
            entry.grateful = request.form.get("grateful")
            # db.session.save(entry)
        db.session.commit()
    else:
        today = datetime.today().strftime('%Y-%m-%d')
        weekday = datetime.today().weekday()
        entry = Entry.query.filter_by(date=today).first()
        if entry:
            form.headline.data = entry.headline
            form.goals.data = entry.goals
            form.notes.data = entry.notes
            form.grateful.data = entry.grateful
            form.edate=entry.date
    return render_template("newhome.html", form=form, data=news, weekday=weekdays[weekday])

@app.route("/date/<datee>")
def date(datee):
    form = EntryForm()
    entry = Entry.query.filter_by(date=datee).first()
    if entry:
        form.headline.data = entry.headline
        form.goals.data = entry.goals
        form.notes.data = entry.notes
        form.grateful.data = entry.grateful
        data  = json.dumps({"goals" : entry.goals, "notes" : entry.notes, "grateful" : entry.grateful, "headline":entry.headline  })
    else:
        data = json.dumps({"goals": '', "notes": '', "headline": ''})
    return data

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True)


