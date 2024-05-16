import sqlite3
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, URLField, IntegerField, SelectField
import wtforms.form as forms
from wtforms.validators import DataRequired, Length, URL, Regexp, Optional


def get_categories():
    connect = sqlite3.connect('./database.db')
    connect.row_factory = sqlite3.Row
    all_categories = connect.execute('SELECT c.cat\
                            FROM categories c ORDER BY c.cat').fetchall()
    connect.close()

    categories = []
    for cat in all_categories:
        categories.append(cat['cat'])

    return categories


class AppForm(FlaskForm):
    name = StringField('AppName', validators=[DataRequired(), Length(min=3, max=15)])
    category = SelectField('Category', validators=[DataRequired(), ], choices=get_categories())
    description = StringField('Description', validators=[DataRequired(), ])
    internal_url = URLField('Internal Url', validators=[DataRequired(), URL()])
    external_url = URLField('External Url', validators=[DataRequired(), URL()])
    icon = StringField('Icon', validators=[DataRequired(), ])
    tags = StringField('Tags (Separate multiple tags with a comma).',
                       validators=[Regexp(r'[^,\s][^\,]*[^,\s]*', message='Tags must contain letters only separated '
                                                                          'by commas.'),
                                   Length(min=3, max=35)])
    extras = TextAreaField("Extras")

    submit = SubmitField('Update')
