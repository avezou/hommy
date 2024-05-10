import sqlite3
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, URLField, IntegerField, SelectField
import wtforms.form as forms
from wtforms.validators import DataRequired, Length, URL, Regexp
from flask_wtf.file import FileField, FileAllowed, FileRequired


def getCategories():
    connect = sqlite3.connect('./database.db')
    connect.row_factory = sqlite3.Row
    allCategories = connect.execute('SELECT c.cat\
                            FROM categories c ORDER BY c.cat').fetchall()
    connect.close()

    categories = []
    for cat in allCategories:
        categories.append(cat['cat'])
        print ("category: " + cat['cat'])

    return categories

class AppForm(FlaskForm):
    name = StringField('AppName', validators=[DataRequired(), Length(min=3, max=15)])
    category = SelectField('Category', validators=[DataRequired(),], choices=getCategories())
    description = StringField('Description')
    internal_url = URLField('Internal Url', validators=[DataRequired(), URL()])
    external_url = URLField('External Url', validators=[DataRequired(), URL()])
    icon = FileField('Icon', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'ico', 'gif', 'webp', 'svg'], 'Images only!')])
    tag1 = StringField('Tag 1', validators=[Regexp('^\w+$', message='Tags must contain letters only'), Length(min=3, max=8)])
    tag2 = StringField('Tag 2', validators=[Regexp('^\w+$', message='Tags must contain letters only'), Length(min=3, max=8)])
    tag3 = StringField('Tag 3', validators=[Regexp('^\w+$', message='Tags must contain letters only'), Length(min=3, max=8)])
    extras = TextAreaField("Extras")

    submit = SubmitField('Update')


