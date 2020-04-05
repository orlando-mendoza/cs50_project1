from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, RadioField, TextAreaField, validators
from wtforms.validators import DataRequired, Email, Length, EqualTo, ValidationError, Optional
from application import db

class LoginForm(FlaskForm):
    email = StringField("Email", validators=[DataRequired(), Email()])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=15)])
    remember_me = BooleanField("Remember Me")
    submit = SubmitField("Login")

class RegisterForm(FlaskForm):
   email = StringField("Email", validators=[DataRequired(), Email()])
   password = PasswordField("Password", validators=[DataRequired(), Length(min=6, max=15)])
   password_confirm = PasswordField("Confirm Password", validators=[DataRequired(), Length(min=6, max=15), EqualTo('password')])
   first_name = StringField("First Name", validators=[DataRequired(), Length(min=2, max=55)])
   last_name = StringField("Last Name", validators=[DataRequired(), Length(min=2, max=55)])
   submit = SubmitField("Register Now")

   def validate_email(self, email):
       if db.execute("SELECT email FROM users WHERE email = :email", {"email": email.data}).rowcount != 0:
           raise ValidationError("Email is already in use. Pick another one.")

class ReviewForm(FlaskForm):
    rate = RadioField(choices=[(1, '1'),(2, '2'), (3, '3'), (4, '4'), (5, ' 5')])
    review = TextAreaField(u'Write a review.', render_kw={'class': 'form-control |', 'rows': 5}, validators=[Length(max=300)])
    submit = SubmitField("Submit")
