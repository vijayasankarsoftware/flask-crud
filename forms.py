from flask_wtf import FlaskForm
from wtforms import StringField, DateField, RadioField, FileField, SubmitField
from wtforms.validators import DataRequired, Email

class UserForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    dob = DateField('Date of Birth', validators=[DataRequired()])
    gender = RadioField('Gender', choices=[('M', 'Male'), ('F', 'Female')], validators=[DataRequired()])
    image = FileField('Profile Picture', validators=[DataRequired()])
    submit = SubmitField('Submit')
