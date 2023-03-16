from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField, FileField
from wtforms.validators import DataRequired, EqualTo, ValidationError, Length
from flask import flash
from app.models import User

#form for login
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember me')
    submit = SubmitField('Sign In')

#form for account creation
class SignupForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:        #username matches with one in a database
            raise ValidationError("Username already taken.")

#form for home page posts               <--- just beginning, not completed
class PostForm(FlaskForm):
    message = TextAreaField('Enter a message', validators = [DataRequired()])
    post = SubmitField('Post')

#form for profile editing
class EditProfileForm(FlaskForm):
    #picture = FileField('Profile Picture')
    newUsername = StringField('New Username')
    newPassword = PasswordField('New Password')
    confirmPassword = PasswordField('Confirm Changes Using Password', validators=[DataRequired()])
    newBio = TextAreaField('Bio', validators=[Length(min=0, max=250)]) #max bio length 250 char
    submit = SubmitField('Confirm')

    '''
    def validate_newUsername(self, newUsername):
        user = User.query.filter_by(username=newUsername.data).first_or_404()
        if user is not None:
            raise ValidationError('Choose another username.')
    '''
            
class SearchForm(FlaskForm):
    search = StringField('Search For User', validators = [DataRequired()])
    submit = SubmitField('Search')

    def validate_search(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is None:        #username does not match with one in a database
            raise ValidationError("There is no such user.")

#form for private messaging
class MessageForm(FlaskForm):
    message = StringField('Enter a message', validators = [DataRequired()])
    enter = SubmitField('Enter')
