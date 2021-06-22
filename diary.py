import os

from flask import Flask
from flask import render_template
from flask import request, redirect, url_for
from datetime import date, datetime
from flask_bootstrap import Bootstrap
from flask_datepicker import datepicker
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, SelectField
from wtforms.validators import DataRequired
from wtforms.fields import DateField
from flask_sqlalchemy import SQLAlchemy
import json
from GoogleNews import GoogleNews
from flask_migrate import Migrate

googlenews = GoogleNews(period='7d',lang='en')
weekdays = ['MONDAY','TUESDAY','WEDNESDAY','THURSDAY','FRIDAY','SATURDAY','SUNDAY']

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "diary.db"))

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = database_file

db = SQLAlchemy(app)
migrate = Migrate(app, db)
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
        return "<Date: {}>".format(self.date)

class EntryForm(FlaskForm):
    edate = DateField('Date',format='%Y-%m-%d', id='datepicker', validators=[DataRequired()], default = date.today)
    grateful = TextAreaField('Grateful',render_kw={"class": "h6 mb-0 font-weight-bold text-gray-800 w-100","contenteditable":"true","aria-multiline":"true"})
    headline = StringField('Headline', render_kw={"class": "h6 mb-0 font-weight-bold text-gray-800 w-100"})
    goals = TextAreaField('Goals',render_kw={"class": "h6 mb-0 font-weight-bold text-gray-800 w-100","contenteditable":"true","aria-multiline":"true"})
    notes = TextAreaField('Notes',render_kw={"class": "h6 mb-0 font-weight-bold text-gray-800 w-100","contenteditable":"true","aria-multiline":"true"})
    submit = SubmitField('Save...')

class Goal(db.Model):
    year = db.Column(db.String(), unique=True, nullable=False, primary_key=True)
    yearly =  db.Column(db.Text())
    quarter1 = db.Column(db.Text())
    quarter2 = db.Column(db.Text())
    quarter3 = db.Column(db.Text())
    quarter4 = db.Column(db.Text())

    january = db.Column(db.Text())
    february = db.Column(db.Text())
    march = db.Column(db.Text())
    april = db.Column(db.Text())
    may = db.Column(db.Text())
    june = db.Column(db.Text())
    july = db.Column(db.Text())
    august = db.Column(db.Text())
    september = db.Column(db.Text())
    october = db.Column(db.Text())
    november = db.Column(db.Text())
    december = db.Column(db.Text())

    def __repr__(self):
        return "<Year: {}>".format(self.year)

class GoalsForm(FlaskForm):
    year = SelectField('', choices=[('2021', '2021'), ('2022', '2022'), ('2023', '2023'), ('2024', '2024'), ('2025', '2025'), ('2026', '2026')])
    yearly = TextAreaField('Grateful',render_kw={"class": "h6 mb-0 font-weight-bold text-gray-800 w-100","contenteditable":"true","aria-multiline":"true"})
    quarter1 = TextAreaField('Grateful',render_kw={"class": "h6 mb-0 font-weight-bold text-gray-800 w-100","contenteditable":"true","aria-multiline":"true"})
    quarter2 = TextAreaField('Grateful',render_kw={"class": "h6 mb-0 font-weight-bold text-gray-800 w-100","contenteditable":"true","aria-multiline":"true"})
    quarter3 = TextAreaField('Grateful',render_kw={"class": "h6 mb-0 font-weight-bold text-gray-800 w-100","contenteditable":"true","aria-multiline":"true"})
    quarter4 = TextAreaField('Grateful',render_kw={"class": "h6 mb-0 font-weight-bold text-gray-800 w-100","contenteditable":"true","aria-multiline":"true"})

    january = TextAreaField('Grateful',render_kw={"class": "h6 mb-0 font-weight-bold text-gray-800 w-100","contenteditable":"true","aria-multiline":"true"})
    february = TextAreaField('Grateful',render_kw={"class": "h6 mb-0 font-weight-bold text-gray-800 w-100","contenteditable":"true","aria-multiline":"true"})
    march = TextAreaField('Grateful',render_kw={"class": "h6 mb-0 font-weight-bold text-gray-800 w-100","contenteditable":"true","aria-multiline":"true"})
    april = TextAreaField('Grateful',render_kw={"class": "h6 mb-0 font-weight-bold text-gray-800 w-100","contenteditable":"true","aria-multiline":"true"})
    may = TextAreaField('Grateful',render_kw={"class": "h6 mb-0 font-weight-bold text-gray-800 w-100","contenteditable":"true","aria-multiline":"true"})
    june = TextAreaField('Grateful',render_kw={"class": "h6 mb-0 font-weight-bold text-gray-800 w-100","contenteditable":"true","aria-multiline":"true"})
    july = TextAreaField('Grateful',render_kw={"class": "h6 mb-0 font-weight-bold text-gray-800 w-100","contenteditable":"true","aria-multiline":"true"})
    august = TextAreaField('Grateful',render_kw={"class": "h6 mb-0 font-weight-bold text-gray-800 w-100","contenteditable":"true","aria-multiline":"true"})
    september = TextAreaField('Grateful',render_kw={"class": "h6 mb-0 font-weight-bold text-gray-800 w-100","contenteditable":"true","aria-multiline":"true"})
    october = TextAreaField('Grateful',render_kw={"class": "h6 mb-0 font-weight-bold text-gray-800 w-100","contenteditable":"true","aria-multiline":"true"})
    november = TextAreaField('Grateful',render_kw={"class": "h6 mb-0 font-weight-bold text-gray-800 w-100","contenteditable":"true","aria-multiline":"true"})
    december = TextAreaField('Grateful',render_kw={"class": "h6 mb-0 font-weight-bold text-gray-800 w-100","contenteditable":"true","aria-multiline":"true"})
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
            # form.edate=today
    return render_template("newhome.html", form=form, data=news, weekday=weekdays[weekday], goals_url="goals/"+str(datetime.now().year))


@app.route("/goals/<year>", methods=["GET", "POST"])
@app.route("/goals", defaults={'year': None}, methods=["POST"])
def goals(year):
    form = GoalsForm()

    if form.validate_on_submit():
        goal = Goal.query.filter_by(year=request.form.get("year")).first()
        if goal == None:
            goal = Goal(year=request.form.get("year"),yearly=request.form.get("yearly"),
                         quarter1=request.form.get("quarter1"),quarter2=request.form.get("quarter2"),
                         quarter3=request.form.get("quarter3"), quarter4=request.form.get("quarter4"),
                         january=request.form.get("january"), february=request.form.get("february"),
                         march=request.form.get("march"), april=request.form.get("april"),
                         may=request.form.get("may"), june=request.form.get("june"),
                         july=request.form.get("july"), august=request.form.get("august"),
                         september=request.form.get("september"), october=request.form.get("october"),
                         november=request.form.get("november"), december=request.form.get("december")
                         )
            db.session.add(goal)
        else:
            goal.yearly = request.form.get("yearly")
            goal.quarter1=request.form.get("quarter1")
            goal.quarter2 = request.form.get("quarter2")
            goal.quarter3 = request.form.get("quarter3")
            goal.quarter4 = request.form.get("quarter4")
            goal.january = request.form.get("january")
            goal.february = request.form.get("febuary")
            goal.march = request.form.get("march")
            goal.april = request.form.get("april")
            goal.may = request.form.get("may")
            goal.june = request.form.get("june")
            goal.july = request.form.get("july")
            goal.august = request.form.get("august")
            goal.september = request.form.get("september")
            goal.october = request.form.get("october")
            goal.november = request.form.get("november")
            goal.december = request.form.get("december")
        db.session.commit()

    else:
        if not year:
            year = datetime.now().year
        goals = Goal.query.filter_by(year=year).first()
        form.year.data = year
        if goals:
            form.yearly.data = goals.yearly
            form.quarter1.data = goals.quarter1
            form.quarter2.data = goals.quarter2
            form.quarter3.data = goals.quarter3
            form.quarter4.data = goals.quarter4
            form.january.data = goals.january
            form.february.data = goals.february
            form.march.data = goals.march
            form.april.data = goals.april
            form.may.data = goals.may
            form.june.data = goals.june
            form.july.data = goals.july
            form.august.data = goals.august
            form.september.data = goals.september
            form.october.data = goals.october
            form.november.data = goals.november
            form.december.data = goals.december

    return render_template("goals.html", form=form)



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


