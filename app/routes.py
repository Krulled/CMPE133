from app import plant_app, db
from flask import render_template, redirect, flash, request, url_for, session
from app.forms import LoginForm, SignupForm, PostForm, EditProfileForm, CommentForm, SearchForm
from app.models import User, Post, Comment, Collection
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import current_user, login_required, login_user, logout_user
import requests

import urllib.request, json
import os                                       # for saving images 
from werkzeug.utils import secure_filename      # for getting absolute path of image

# import phonenumbers # library to validate phone number, unused for ease of testing

#timeout stuff
from datetime import timedelta

''' CONFIG FOR UPLOADING IMAGES TO POSTS '''
plant_app.config['SECRET_KEY'] = 'you-will-never-guess'
plant_app.config['POST_UPLOAD_FOLDER'] = 'static/post_images'
plant_app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.jpeg', '.png'] 
''' CONFIG FOR UPLOADING PROFILE PICTURES '''
plant_app.config['PROFILE_UPLOAD_FOLDER'] = 'static/css/profile_images' 

'''
added this method for session timeout
if user is inactive for 15 minutes (no route changes), timeout session
'''
@plant_app.before_request
def before_request():
    session.permanent = True
    plant_app.permanent_session_lifetime = timedelta(minutes=15) 

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
       
            '''-IMAGE HANDLING-'''
        file = current_form.profilepic.data   # from PostForm
        sec_filename = secure_filename(file.filename)
        if sec_filename != '':
            file_ext = os.path.splitext(sec_filename)[1] # file type (ex. .png, .jpg, .gif)
            if file_ext not in plant_app.config['UPLOAD_EXTENSIONS']:
                flash('Uploaded image type is not supported (allowed types: jpg, png, jpeg)')
                redirect("signup")
            # fell through--save file locally and commit filename to DB
            print(sec_filename)
            ''' 
            saves image locally by using the absolute path created from
            joining the project directory's path, the upload folder path,
            and the name of the file as a secure filename
            '''
            user.set_profilepic(sec_filename)
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                plant_app.config['PROFILE_UPLOAD_FOLDER'],
                sec_filename))
        else:   # no image chosen
            sec_filename = None
        '''----------------'''
        user.set_profilepic(sec_filename)
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
    form = SearchForm()
    user = User.query.filter_by(username=username).first_or_404()
    #filter posts by author and descending order by time
    list_of_posts = Post.query.filter_by(author=user).order_by(Post.time_posted.desc()).all() #Post.query.all()
    return render_template('profile.html', user=user, list_of_posts=list_of_posts, form=form)

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
          
            '''-IMAGE HANDLING-'''
        file = current_form.newPicture.data   # from PostForm
        sec_filename = secure_filename(file.filename)
        if sec_filename != '':
            file_ext = os.path.splitext(sec_filename)[1] # file type (ex. .png, .jpg, .gif)
            if file_ext not in plant_app.config['UPLOAD_EXTENSIONS']:
                flash('Uploaded image type is not supported (allowed types: jpg, png, jpeg)')
                redirect(url_for('edit', username=username))
            # fell through--save file locally and commit filename to DB
            print(sec_filename)
            ''' 
            saves image locally by using the absolute path created from
            joining the project directory's path, the upload folder path,
            and the name of the file as a secure filename
            '''
            user.set_profilepic(sec_filename)
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                plant_app.config['PROFILE_UPLOAD_FOLDER'],
                sec_filename))
        else:   # no image chosen
            sec_filename = None
        '''----------------'''

        if len(current_form.newPassword.data) != 0:
            user.set_password(current_form.newPassword.data)
            flash('Password changed!')
            db.session.commit()

        if len(current_form.newEmail.data) != 0:
            user.set_email(current_form.newEmail.data)
            flash('Email changed!')
            db.session.commit()

        if len(current_form.newPhone.data) != 0:
            # phoneNumber = phonenumbers.parse(current_form.newPhone.data)
            # if phonenumbers.is_possible_number(phoneNumber):
            user.set_phone(current_form.newPhone.data)
            flash('Phone number changed!')
            db.session.commit()
            # else:
            #     flash('Phone number is not valid, change not saved.')
        if len(current_form.newPicture.data.filename) != 0:
            user.set_profilepic(current_form.newPicture.data.filename)
            flash('profile pic changed!')
            db.session.commit()
        return redirect(url_for('login'))

    return render_template('edit.html' ,user=user, form=current_form)

#search user
# @plant_app.route('/user/<username>/search', methods=['POST', 'GET'])
# @login_required
# def search(username):
#     current_form = SearchUsersForm()

#     #On submission, checks if data is acccepted by all field validators
#     if current_form.validate_on_submit():
#         if(current_form.search.data == current_user.username):
#             flash("You cannot search for yourself!")
#             return redirect(url_for('search', username = current_user.username))

#         user = User.query.filter_by(username=current_form.search.data).first()
#         return render_template(('searchResults.html'), form = current_form, username = user.username)

#     return render_template('search.html', user=username, form= current_form)

#search profile
@plant_app.route('/user/searchProfile/<username>', methods=['POST', 'GET'])
@login_required
def searchProfile(username):
    user = User.query.filter_by(username=username).first()
    return render_template('search_profile.html', username=user)

#search plant
@plant_app.route('/user/searchPlant/<username>', methods=['POST', 'GET'])
@login_required
def searchPlant(username):
    user = User.query.filter_by(username=username).first()
    url = "https://perenual.com/api/species-list?page=1&key=sk-CwED63eab143ecfef46&q={}"
    response = urllib.request.urlopen(url)
    data = response.read()
    dict = json.loads(data)

    plants = []

    for plant in dict["results"]:
        plant = {
            "name": plant["name"],
            "picture": plant["picture"]
        }

        plants.append(plant)

    return render_template('search_plant.html', username=user)

#view user home page with calendar
@plant_app.route('/user/<username>/home', methods = ['POST', 'GET'])
@login_required
def home(username):
    form = SearchForm()
    user = User.query.filter_by(username=username).first_or_404()
    collections = Collection.query.filter_by(user_id=user.id)
    plant_ids = [c.plant_id for c in collections]
    plant_data = []
    for plant_id in plant_ids:
        api_url = f'https://perenual.com/api/species/details/{plant_id}?key=sk-CwED63eab143ecfef46'
        response = requests.get(api_url)
        if response.status_code == 200:
            plant = response.json()
            # Get the start date for this plant from the collection
            collection = Collection.query.filter_by(user_id=user.id, plant_id=plant['id']).first()
            if collection:
                plant['start_date'] = collection.start_date
            else:
                plant['start_date'] = None
            plant_data.append(plant)
    events = []
    for plant in plant_data:
        startDate = plant['start_date'].strftime('%Y-%m-%d')
        if (plant['watering'] == 'Frequent'):
            recurring = 'FREQ=WEEKLY;BYDAY=MO,FR'
        elif (plant['watering'] == 'Average'):
            recurring = 'FREQ=WEEKLY'
        else:
            recurring = 'FREQ=MONTHLY'
        dict = {
            'plant': plant['common_name'],
            'startDate': startDate,
            'recurring' : recurring
        }
        events.append(dict)
        print(dict['recurring'])
    return render_template('home.html', user=user, form=form, plant_data=plant_data, events=events)

#view forum page (aka view all posts)
@plant_app.route('/user/<username>/forum', methods = ['POST', 'GET'])
@login_required
def forum(username):
    form = SearchForm()
    list_of_posts = Post.query.order_by(Post.time_posted.desc()).all() #Post.query.all()
    # current_form = PostForm()
    # user = User.query.filter_by(username=username).first_or_404()
    # #messages = Message.query.filter_by(user_id=user.id).all()
    return render_template('forum.html', list_of_posts=list_of_posts, form=form )

#create a new post
@plant_app.route('/user/<username>/post/new', methods = ['POST', 'GET'])
@login_required
def new_post(username):
    current_form = PostForm()
    if current_form.validate_on_submit():
        '''-IMAGE HANDLING-'''
        file = current_form.file.data   # from PostForm
        sec_filename = secure_filename(file.filename)
        if sec_filename != '':
            file_ext = os.path.splitext(sec_filename)[1] # file type (ex. .png, .jpg, .gif)
            if file_ext not in plant_app.config['UPLOAD_EXTENSIONS']:
                flash('Uploaded image type is not supported (allowed types: jpg, png, jpeg)')
                redirect('new_post')
            # fell through--save file locally and commit filename to DB
            print(sec_filename)
            ''' 
            saves image locally by using the absolute path created from
            joining the project directory's path, the upload folder path,
            and the name of the file as a secure filename
            '''
            file.save(os.path.join(os.path.abspath(os.path.dirname(__file__)),
                plant_app.config['POST_UPLOAD_FOLDER'],
                sec_filename))
        else:   # no image chosen
            sec_filename = None
        '''----------------'''
        post = Post(post_title=current_form.title.data, post_content=current_form.message.data, 
                    author=current_user, image=sec_filename) 
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success') # 'success' is a category for bootstrap, is optional
        return redirect(url_for('forum', username = current_user.username))
    return render_template('create_post.html', title='New Post', form=current_form, legend='New Post')

# view a post (from the forum)
@plant_app.route('/post/<int:post_id>', methods = ['POST', 'GET'])
@login_required     # now forced to make login required for viewing posts
def post(post_id):
    post = Post.query.get_or_404(post_id)
    post_comments = Post.query.get_or_404(post_id).comments.all()     # intended to display all comments replying to the current post
    '''-IMAGE HANDLING-'''
    if post.image != None:
        image_rel_path = '/static/post_images/' + post.image  
        print(image_rel_path)
    else: image_rel_path = None
    '''----------------'''
    current_form = CommentForm()
    if current_form.validate_on_submit():
        comment = Comment(author=current_user, comment_content=current_form.comment_content.data, post_id=post_id)
        db.session.add(comment)
        db.session.commit()
        flash('Your comment has been posted!', 'success')       # displays at the bottom of the comments page, should be moved
        return redirect(url_for('post', post_id=post_id))
    return render_template('post.html', post=post, form=current_form,
                            post_comments=post_comments, image=image_rel_path)

@plant_app.route('/search', methods = ['GET', 'POST'])
@login_required
def search():
    form = SearchForm()
    if form.validate_on_submit():
        if request.method == 'POST':
            query = form.searched.data
            api_url = "https://perenual.com/api/species-list?key=sk-CwED63eab143ecfef46&q=" + query
            response = requests.get(api_url)
            data = response.json()
            return render_template('search.html', data=data, search = query, form=form, username=current_user.username)
    else:
        flash("You didn't search anything!")
    return redirect(url_for('home', username = current_user.username))

@plant_app.route('/user/<username>/collection')
@login_required
def collection(username):
    form = SearchForm()
    user = User.query.filter_by(username=username).first()
    collections = Collection.query.filter_by(user_id=user.id)
    plant_id = [c.plant_id for c in collections]
    plant_data = []
    for plant_id in plant_id:
        api_url = f'https://perenual.com/api/species/details/{plant_id}?key=sk-CwED63eab143ecfef46'
        response = requests.get(api_url)
        if response.status_code == 200:
            plant_data.append(response.json())   
    return render_template('collection.html', user=user, username=current_user.username, form=form, plant_data=plant_data)

@plant_app.route('/user/<username>/add-to-collection', methods = ['POST'])
@login_required
def add_to_collection(username):
    plant_id = request.form.get('plant_id')
    user = User.query.filter_by(username=username).first()
    collection_item = Collection(plant_id=plant_id, user_id=user.id)
    db.session.add(collection_item)
    db.session.commit()
    flash('Successfully added to collection. ')
    return redirect(url_for('collection', username=current_user.username))

@plant_app.route('/user/<username>/remove-from-collection', methods=['POST'])
@login_required
def delete_from_collection(username):
    plant_id = request.form.get('plant_id')
    collection_item = Collection.query.filter_by(plant_id=plant_id).first()
    db.session.delete(collection_item)
    db.session.commit()
    flash('Item deleted!')
    return redirect(url_for('collection', username=current_user.username))
