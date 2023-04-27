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
    username = StringField('Username', validators=[DataRequired(message="Username required.")])
    password = PasswordField('Password', validators=[DataRequired(message="Password required.")])
    confirmPassword = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Password must match.')])
    email = StringField('Email', validators=[DataRequired(message="Email required.")])
    phone = StringField('Phone Number (Optional)', validators=None)
    submit = SubmitField('Register')
    profilepic = FileField("Choose File")

    def validate_username(self, username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:        #username matches with one in a database
            raise ValidationError("Username already taken.")
        
    def validate_email(self, email):
        email = User.query.filter_by(email = email.data).first()
        if email is not None:        #email matches with one in a database
            raise ValidationError("Email already taken.")

#form for home page posts               
class PostForm(FlaskForm):
    title = StringField('Title:', validators = [DataRequired()])
    message = TextAreaField('Message:', validators = [DataRequired()])
    submit_post = SubmitField('Post')

class CommentForm(FlaskForm):
    comment_content = TextAreaField('Comment:', validators=[DataRequired()])
    submit_comment = SubmitField('Post Comment')

#form for profile editing
class EditProfileForm(FlaskForm):
    newPicture = FileField('Profile Picture')
    #newUsername = StringField('New Username')
    newPassword = PasswordField('New Password')
    confirmPassword = PasswordField('Confirm Changes Using Password', validators=[DataRequired()])
    newEmail = StringField('New Email')
    newPhone = StringField('New Phone')
    #newBio = TextAreaField('Bio', validators=[Length(min=0, max=250)]) #max bio length 250 char
    submit = SubmitField('Confirm')

#form for searching users         
# class SearchUsersForm(FlaskForm):
#     search = StringField('Search For User', validators = [DataRequired()])
#     submit = SubmitField('Search')

#     def validate_search(self, username):
#         user = User.query.filter_by(username = username.data).first()
#         if user is None:        #username does not match with one in a database
#             raise ValidationError("There is no such user.")

class SearchForm(FlaskForm):
    searched = StringField('Search For User', validators = [DataRequired()])
    submit = SubmitField('Search')
