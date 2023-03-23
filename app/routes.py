from app import plant_app, db
from flask import render_template, redirect, flash, request, url_for
from app.forms import LoginForm, SignupForm, PostForm, EditProfileForm, SearchUsersForm
from app.models import User #, Message #, Post
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_required, login_user, logout_user


@plant_app.before_first_request
def create_tables():
    db.create_all()

#login
@plant_app.route('/', methods=['POST', 'GET'])
def login():
    #if user is already logged in
    if current_user.is_authenticated:
        return redirect(url_for('home', username = current_user.username))

    current_form = LoginForm()
    # taking input from the user and doing somithing with it
    if current_form.validate_on_submit():
        # search to make sure we have the user in our database
        user = User.query.filter_by(username=current_form.username.data).first()

        # check user's password with what is saved on the database
        if user is None or not user.check_password(current_form.password.data): 
            flash('Invalid password!')
            # if passwords don't match, send user to login again
            return redirect(url_for('login'))

        # login user
        login_user(user, remember=current_form.remember_me.data)
        print(current_form.username.data, current_form.password.data)

        #if login is successful, go to home page with username in url
        return redirect(url_for('home', username = current_form.username.data))
    return render_template('login.html', form=current_form)

#create an account
@plant_app.route('/signup', methods = ['POST', 'GET'])
def signup():
    if current_user.is_authenticated:
        return redirect(url_for('home', username = current_user.username))           #if user is logged in, go to homepage
    current_form = SignupForm()

    #On submission, checks if data is acccepted by all field validators
    if current_form.validate_on_submit():
        user = User(username=current_form.username.data)
        user.set_password(current_form.password.data)
        user.set_email(current_form.email.data)
        if len(current_form.phone.data) != 0:
            user.set_phone(current_form.phone.data) 
        if len(current_form.profilepic.data) != 0:
            user.set_profilepic(current_form.profilepic.data) 
        db.session.add(user)
        db.session.commit()
        flash('Account creation successful!')
        return redirect(url_for('login'))
    return render_template('signup.html', form=current_form)

#logout
@plant_app.route('/logout')
@login_required
def logout():
    if current_user.is_authenticated:
        logout_user()
        flash('You have logged out')
        return redirect(url_for('login'))
    else:
        return redirect(url_for('login'))

#delete confirmation
@plant_app.route('/user/<username>/deleteConfirm', methods=['POST', 'GET'])
@login_required
def deleteConfirm(username):
    user = User.query.filter_by(username=username).first()
    return render_template('delete.html', user=user)

#delete account
@plant_app.route('/user/<username>/delete', methods=['POST', 'GET'])
@login_required
def delete(username):
    user = User.query.filter_by(username=username).first_or_404()
    db.session.delete(user)
    db.session.commit()
    flash('Account deleted successfully')
    return redirect(url_for('login'))    #redirect to login

#user profile 
@plant_app.route('/user/<username>/profile/')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', user=user)

#edit profile
@plant_app.route('/user/<username>/profile/edit', methods=['POST', 'GET'])
@login_required
def edit(username):
    user = User.query.filter_by(username=username).first()
    current_form = EditProfileForm()
    if current_form.validate_on_submit():
        # check user's password with what is saved on the database
        if not user.check_password(current_form.confirmPassword.data):
            flash('Incorrect password, changes not saved.')
            # if passwords don't match, send user to edit again
            return redirect(url_for('edit', username=username))

<<<<<<< HEAD
<<<<<<< HEAD
        if current_form.newPicture.data != None:
            user.set_profilepic(current_form.newPicture.data)
            flash('Picture changed!')
=======
        if len(current_form.newPicture.data) != 0:
            user.set_profilePic(current_form.newPicture.data)
            flash('Password changed!')
>>>>>>> 79baa99 (adding profile png data to user database)
=======
        if len(current_form.newPicture.data) != 0:
            user.set_profilePic(current_form.newPicture.data)
            flash('Password changed!')
>>>>>>> 08d67ee (changes)
            db.session.commit()
        
        if len(current_form.newPassword.data) != 0:
            user.set_password(current_form.newPassword.data)
            flash('Password changed!')
            db.session.commit()

        return redirect(url_for('login'))

    return render_template('edit.html' ,user=user, form=current_form)

#view followers
@plant_app.route('/user/<username>/followers')
@login_required
def followers(username):
    user = User.query.filter_by(username=username).first()
    num = 0
    for followers in user.followers:
        num += 1
    return render_template('followers.html', user=user, num = num)

#search user
@plant_app.route('/user/<username>/search', methods=['POST', 'GET'])
@login_required
def search(username):
    current_form = SearchUsersForm()

    #On submission, checks if data is acccepted by all field validators
    if current_form.validate_on_submit():
        if(current_form.search.data == current_user.username):
            flash("You cannot search for yourself!")
            return redirect(url_for('search', username = current_user.username))

        user = User.query.filter_by(username=current_form.search.data).first()
        return render_template(('searchResults.html'), form = current_form, username = user.username)

    return render_template('search.html', user=username, form= current_form)

#search profile
@plant_app.route('/user/searchProfile/<username>', methods=['POST', 'GET'])
@login_required
def searchProfile(username):
    user = User.query.filter_by(username=username).first()
    return render_template('searchProfile.html', username=user)

#follow
@plant_app.route('/user/searchProfile/<username>/follow', methods=['POST', 'GET'])
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    #user does not exist, here bc some people might edit links
    if user is None:
        flash("User does not exist")
        return redirect(url_for('search', username = current_user.username))
    else:
        current_user.follow(user)
        db.session.commit()
        return redirect(url_for('searchProfile',username = username))

#unfollow 
@plant_app.route('/user/searchProfile/<username>/unfollow', methods=['POST', 'GET'])
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()

    #user does not exist, here bc some people might edit links
    if user is None:
        flash("User does not exist")
        return redirect(url_for('search', username = current_user.username))
    else:
        current_user.unfollow(user)
        db.session.commit()
        return redirect(url_for('searchProfile',username = username))

#view user home page
@plant_app.route('/user/<username>/home', methods = ['POST', 'GET'])
@login_required
def home(username):
    #current_form = PostForm()
    user = User.query.filter_by(username=username).first_or_404()
    #messages = Message.query.filter_by(user_id=user.id).all()
    return render_template('home.html', user=user) #, messages=messages)

#view forum page
@plant_app.route('/user/<username>/forum', methods = ['POST', 'GET'])
@login_required
def forum(username):
    current_form = PostForm()
    user = User.query.filter_by(username=username).first_or_404()
    #messages = Message.query.filter_by(user_id=user.id).all()
    return render_template('forum.html', user=user, form = current_form) #, messages=messages)