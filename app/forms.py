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
    #creating fields for signing up
    username = StringField('Username', validators=[DataRequired(message="Username required.")])
    password = PasswordField('Password', validators=[DataRequired(message="Password required.")])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Password must match.')])
    email = StringField('Email', validators=[DataRequired(message="Email required.")])
    phone = StringField('Phone Number (Optional)', validators=None)
    profilepic = FileField('Upload Image')
    submit = SubmitField('Register')

    #validate username to see if there is already that user name in the database; ensure unique username
    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:        #username matches with one in a database
            raise ValidationError("Username already taken.")
        
    #validate email to ensure unique email
    def validate_email(self, email):
        email = User.query.filter_by(email = email.data).first()
        if email is not None:        #email matches with one in a database
            raise ValidationError("Email already taken.")

#form for forum posts               
class PostForm(FlaskForm):
    #creating fields for posting
    title = StringField('Title:', validators = [DataRequired()])
    message = TextAreaField('Message:', validators = [DataRequired()])
    file = FileField('Upload Image')
    submit_post = SubmitField('Post')

#form for comments
class CommentForm(FlaskForm):
    #creating fields for commenting
    comment_content = TextAreaField('Comment:', validators=[DataRequired()])
    submit_comment = SubmitField('Post Comment')

#form for profile editing
class EditProfileForm(FlaskForm):
    #creating fields for editing
    newPicture = FileField('Profile Picture')
    newPassword = PasswordField('New Password')
    confirmPassword = PasswordField('Confirm Changes Using Password', validators=[DataRequired()])
    newEmail = StringField('New Email')
    newPhone = StringField('New Phone')
    submit = SubmitField('Confirm')

#form for searching users         
# class SearchUsersForm(FlaskForm):
#     search = StringField('Search For User', validators = [DataRequired()])
#     submit = SubmitField('Search')

#     def validate_search(self, username):
#         user = User.query.filter_by(username = username.data).first()
#         if user is None:        #username does not match with one in a database
#             raise ValidationError("There is no such user.")

#form for searching users and plants
class SearchForm(FlaskForm):
    #creating fields for searching
    searched = StringField('Search For User', validators = [DataRequired()])
    submit = SubmitField('Search')
