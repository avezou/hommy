from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, BooleanField, URLField, IntegerField
import wtforms.form as forms
from wtforms.validators import DataRequired, Length, URL, Regexp
from flask_wtf.file import FileField, FileAllowed, FileRequired

class AppForm(FlaskForm):
    name = StringField('AppName', validators=[DataRequired(), Length(min=3, max=15)])
    category = StringField('Category', validators=[Length(min=2, max=15)])
    description = StringField('Description')
    internal_url = URLField('Internal Url', validators=[DataRequired(), URL()])
    external_url = URLField('External Url', validators=[DataRequired(), URL()])
    icon = FileField('Icon', validators=[FileRequired(), FileAllowed(['jpg', 'jpeg', 'png', 'ico', 'gif', 'webp', 'svg'], 'Images only!')])
    tag1 = StringField('Tag 1', validators=[Regexp('^\w+$', message='Tags must contain letters only'), Length(min=3, max=8)])
    tag2 = StringField('Tag 2', validators=[Regexp('^\w+$', message='Tags must contain letters only'), Length(min=3, max=8)])
    tag3 = StringField('Tag 3', validators=[Regexp('^\w+$', message='Tags must contain letters only'), Length(min=3, max=8)])
    extras = TextAreaField("Extras")

    submit = SubmitField('Update')


