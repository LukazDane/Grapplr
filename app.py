import secrets
from flask import Flask, g
from flask import render_template, flash, redirect, url_for, session, request, abort, send_file
from flask import make_response as response
from forms import FightForm
from werkzeug.utils import secure_filename
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
from peewee import fn
from io import BytesIO
import os
import forms 
import models





#----------------------------
# Oauth2/Rauth stuff
#----------------------------
# twitter_blueprint = make_twitter_blueprint(api_key='', api_secret='')
# github_blueprint = make_github_blueprint(client_id='', client_secret='')

DEBUG = True
PORT = int(os.environ.get('PORT', 9000))

app = Flask(__name__)
app.secret_key = 'elsdhfsdlfdsjfkljdslfhjlds'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:////Users/lukazphelps/Desktop/Grapplr/grapplr.db'
db = SQLAlchemy(app)

#-------------
#Login manager
#-------------
login_manager = LoginManager() # init instance ofhte LoginManager class
login_manager.init_app(app) ## sets up our login for the app
login_manager.login_view = 'login' # setting default login view as the login function

@login_manager.user_loader
def load_user(userid):
    try:
        return models.User.get(models.User.id == userid)
    except models.DoesNotExist:
        return None

# Handle requests when the come in (before) and when they complete (after)
@app.before_request
def before_request():
    # """Connect to the DB before each request."""
    g.db = models.DATABASE
    g.db.connect()
    g.user = current_user

@app.after_request
def after_request(response):
    # """Close the database connection after each request."""
    g.db.close()
    return response

#-----------------
# Root Route
#-----------------
@app.route('/')
def index(name=None):
    if current_user.is_authenticated:
        return redirect(url_for('profile', username=current_user.username))
    else:
        return render_template('landing.html',title="Signin")

@app.route('/signin')
def signin(name=None):
    if current_user.is_authenticated:
        return redirect(url_for('profile', username=current_user.username))
    return render_template('landing.html', title='Sign-In', name=name)

#login
@app.route('/login', methods=['GET','POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('profile', username=current_user.username))
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data) # comparing the user email in the database to the one put in the form
        except models.DoesNotExist:
            flash("no such email/password combination")
        else:   # using the check_password_hash method bc we hashed the user's password when they registered. comparing the user's password in the database to the password put into the form
            if check_password_hash(user.password, form.password.data):
                ## creates session
                login_user(user) # this method comes from the flask_login package
                flash("You've been logged in", "success")
                return redirect('/profile')
            else:
                flash("your email or password doesn't match", "error")
    
    return render_template('login.html', form=form)
    # return render_template('login.html', title="Login", name=name)

#logout
@app.route("/logout")
@login_required
def logout():
    logout_user()
    flash("Logged out successfully", 'success'),
    return redirect(url_for('index'))

#register
@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('profile', username=current_user.username))
    form = forms.RegisterForm()
    if form.validate_on_submit():
        flash("Registration Complete", 'Success')
        models.User.create_user(
            username = form.username.data,
            email = form.email.data,
            password = form.password.data,
            name = form.name.data,
            height = form.height.data,
            weight = form.weight.data,
            style = form.style.data,
            about = form.about.data
            )
        return redirect('/login')
    return render_template('register.html', title="Register", form=form)
#-----------------
# Profile
#-----------------
def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, f_name, f_ext = os.path.splitext(form_picture.filename)
    pictrue_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)
    form_picture.save(picture_path)
    return pictrue_fn

@app.route('/profile/')
@app.route('/profile', methods=['GET','POST'])
@login_required
def profile():
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('profile.html', user=current_user, title=profile, image_file=image_file)

@app.route('/profile/upload')
@login_required
def imgupload():
    return render_template('upload.html')
#image upload
@app.route('/upload', methods=['POST'])
@login_required
def upload():
    form = forms.UploadForm()
    file = request.files['inputFile']
    user = models.User.get(current_user.id)
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        newFile = FileContents(name=file.filename, data=file.read(), user_id=current_user.id, form=form)
        db.session.add(newFile)
        db.session.commit()
        flash('Saved ' + file.filename + ' to the database!')
        return redirect(url_for('profile'), form=form)
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)
    return render_template('upload.html', form=form, image_file=image_file)

#edit profile
@app.route('/editProfile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = forms.UpdateUserForm()
    user = models.User.get(current_user.id)
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.height = form.height.data
        user.weight = form.weight.data
        user.style = form.style.data
        user.about = form.about.data
        user.save()
        flash('Profile has been updated', 'success')
        return redirect(url_for('profile'))
    elif request.method == 'GET':
        form.email.data = current_user.email
        form.username.data = current_user.username
        form.height.data = current_user.height
        form.weight.data = current_user.weight
        form.style.data = current_user.style
        form.about.data = current_user.about
    return render_template('edit_profile.html', form = form)


#--------------
# dash
#--------------
@app.route('/dashboard/')
@app.route('/dashboard', methods=['GET','POST'])
@login_required
def dashboard():
    form = forms.FightForm()
    fights = models.Fight.select()
    if form.validate_on_submit():
        models.Fight.create(
        name=form.name.data.strip(),
        description=form.description.data.strip(), 
        user = current_user.id)
        return redirect(url_for("dashboard.html", user=current_user, form=form, fights=fights))
    return render_template('dashboard.html', user=current_user, form=form, fights=fights)

#delete fight
@app.route("/dashboard/<fightid>")
@login_required
def delete_fight(fightid):
    # form = forms.fightForm()
    fight = models.Fight.get(models.Fight.id == fightid)
    fight.delete_instance()
    return redirect(url_for('dashboard'))

#edit fight
@app.route("/editfight/<fightid>", methods=["GET", "POST"])
@login_required
def edit_fight(fightid):
    fight = models.Fight.get(models.Fight.id == fightid)
    form = forms.FightForm()
    if form.validate_on_submit():
        fight.name = form.name.data
        fight.description = form.description.data
        fight.save()
        fights = models.Fight.select().where(models.Fight.user == current_user.id)
        return redirect(url_for("dashboard", user=current_user, form=form, fights=fights))
    
    form.name.data = fight.name
    form.description.data = fight.description
    return render_template("edit_fight.html", user=current_user, form=form)

#--------------
# swipe
#--------------
@app.route('/swipe/')
@app.route('/swipe', methods=['GET','POST'])
@login_required
def swipe():
    return render_template('swipe.html', user=current_user)

#--------------
# Other Users
#--------------
@app.route('/profile/<username>')
@login_required
def user(username):
    
    fights = [
        {'name': user, 'description': 'Test post #1'},
        {'name': user, 'description': 'Test post #2'}
    ]
    return render_template('profile.html', username='user.username',user=user, fights=fights)


#--------------
# Create fight
#--------------

@app.route('/addfight', methods=['GET', 'POST'])
@login_required
def add_fight():
    form = forms.FightForm()
    fights = models.Fight.select().where(models.Fight.user == current_user.id)
    if form.validate_on_submit():
        models.Fight.create(
        name=form.name.data,
        description=form.description.data.strip(),
        user = current_user.id)
        return redirect(url_for('dashboard', user=current_user, form=form, fights=fights))
    return render_template('add_fight.html', user=current_user, form=form, fights=fights)

#---------------
# Fights
#---------------
@app.route('/fights')
@app.route('/fights/<id>', methods=['GET', 'POST'])
def fights(id=None):
    fight_id = int(id)
    fight = models.Fight.get(models.Fight.id == fight_id)
    return render_template('fight.html'.format(fight_id))

#---------------
# Error handling
#---------------
@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

#---------------------------------------------------------

# --------------------------------------------------------

class FileContents(db.Model): 
    __tablename__= "file_contents"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300), unique=True)
    data = db.Column(db.LargeBinary, unique=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

class User(db.Model):
    __tablename__ = "user"
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String)
    age = db.Column(db.Integer)
    location = db.Column(db.String)
    height = db.Column(db.Integer)
    weight = db.Column(db.Integer)
    style = db.Column(db.String)
    about = db.Column(db.String(450))
    image_file = db.Column(db.String(20), nullable=False, default='tyler2.jpg')

#     def __init__(self, email):
#         self.email = email

#     def __repr__(self):
#         return '<E-mail %r>' % self.email

if __name__ == '__main__':
    models.initialize()
    app.secret_key = os.urandom(12)
    app.run(debug=DEBUG, port=PORT)


