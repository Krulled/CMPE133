from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from app import login
from flask_login import UserMixin

#from datetime import datetime


<<<<<<< HEAD
=======
<<<<<<< HEAD

=======
>>>>>>> 53cebc6 (changes)
>>>>>>> 7cea868 (ch)
#table of followers
followers = db.Table('followers',
            db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
            db.Column('followed_id', db.Integer, db.ForeignKey('user.id')))

#user class
class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(32), unique=True, nullable = False) #dont want username to be null, 32 characters max
    password = db.Column(db.String(32), nullable = False)
    email = db.Column(db.String(64), unique=True, nullable = False)
    phone = db.Column(db.String(11))
    profilepic = db.Column(db.String(), nullable = True)

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
<<<<<<< HEAD
<<<<<<< HEAD
    
    def set_profilepic(self, profilepic):
        self.profilepic = profilepic
<<<<<<< HEAD
=======
    def set_profilepic(self, profilePic):
        self.profile = profilePic
<<<<<<< HEAD
>>>>>>> 79baa99 (adding profile png data to user database)
=======
>>>>>>> 53cebc6 (changes)
<<<<<<< HEAD
>>>>>>> 08d67ee (changes)
=======
=======
    def set_profilepic(self, profilepic):
        self.profilepic = profilepic
>>>>>>> 627f0af (changes1)
>>>>>>> 2123a7d (changes)
=======
>>>>>>> f5df3c8 (changes)
=======
        
    def set_profilepic(self, profilePic):
        self.profile = profilePic
>>>>>>> main
=======
        
<<<<<<< HEAD
<<<<<<< HEAD
<<<<<<< HEAD
    def set_profilepic(self, profilePic):
        self.profile = profilePic
>>>>>>> 6d5c92e (adding profile png data to user database)
=======
    def set_profilepic(self, profilepic):
        self.profilepic = profilepic
>>>>>>> d43a2a6 (changes)
=======
=======
>>>>>>> 5a29eb8 (ch)
    def set_profilepic(self, profilepic):
        self.profilepic = profilepic
=======
    def set_profilepic(self, profilePic):
        self.profile = profilePic
>>>>>>> 53cebc6 (changes)
<<<<<<< HEAD
>>>>>>> 7cea868 (ch)
=======
=======
    def set_profilepic(self, profilepic):
        self.profilepic = profilepic
>>>>>>> 627f0af (changes1)
>>>>>>> 5a29eb8 (ch)

    def __repr__(self):
        return f'<User {self.username}>'


@login.user_loader
def load_user(id):
    return User.query.get(int(id))