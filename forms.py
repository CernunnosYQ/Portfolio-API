from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, Length

class SignUp(FlaskForm):
    username = StringField('username', validators=[DataRequired(), Length(max=64)])
    password = PasswordField('password', validators=[DataRequired()])
    email = StringField('email', validators=[DataRequired(), Email()])
