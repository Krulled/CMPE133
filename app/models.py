from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from flask_login import UserMixin

from datetime import datetime



#table of followers
followers = db.Table('followers',
            db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
            db.Column('followed_id', db.Integer, db.ForeignKey('user.id')))

#post class
class Post(db.Model):
    post_id = db.Column(db.Integer, primary_key = True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable = False)
    post_title = db.Column(db.String(32), nullable = False)
    time_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)       
    post_content = db.Column(db.Text, nullable = False)
    comments = db.relationship('Comment', backref='post', lazy='dynamic')
    # comments should be added as a db relationship (one post to many comments)
    # number_of_likes = db.Column(db.Integer(), nullable = False)

    def __repr__(self):
        return f"Post('{self.post_title}', '{self.time_posted}')"
    '''
    def set_author(self, author_id):
        self.author_id = author_id
    
    def set_post_title(self, post_title):                
        self.post_title = post_title
    
    def set_time_posted(self):
        self.time_posted = datetime.utcnow()
    
    def set_post_content(self, post_content):
        self.post_content = post_content
    '''
#comment class
class Comment(db.Model):
    post_id = db.Column(db.Integer, db.ForeignKey('post.post_id'), nullable=False)
    comment_id = db.Column(db.Integer, primary_key = True)
    author_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    time_posted = db.Column(db.DateTime, nullable = False, default = datetime.utcnow)       
    comment_content = db.Column(db.Text, nullable = False)

#user class
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), unique = True, nullable = False) #dont want username to be null, 32 characters max
    password = db.Column(db.String(32), nullable = False)
    email = db.Column(db.String(64), unique = True, nullable = False)
    phone = db.Column(db.String(11))
    profilepic = db.Column(db.String(256))
    posts = db.relationship('Post', backref='author', lazy=True)
    comments = db.relationship('Comment', backref='author', lazy=True)

    #setting followed and user's relationship
    followed = db.relationship(
        'User', secondary=followers,
        primaryjoin=(followers.c.follower_id == id),
        secondaryjoin=(followers.c.followed_id == id),
        backref=db.backref('followers', lazy='dynamic'), lazy='dynamic')

    #follow
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)

    #unfollow
    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)

    #
    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)

    def set_username(self, username):
        self.username = username

    def set_phone(self, phone):
        self.phone = phone

    def set_email(self, email):
        self.email = email
        
    def set_profilepic(self, profilepic):
        self.profilepic = profilepic

    def __repr__(self):
        return f'<User {self.username}>'

class Collection(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    plant_id = db.Column(db.Integer)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))