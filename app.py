from flask import Flask, g
from flask import render_template, flash, redirect, url_for, session, request, abort 
from flask import make_response as response
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
from flask_dance.contrib.twitter import make_twitter_blueprint, twitter
from flask_dance.contrib.github import make_github_blueprint, github
import os
import forms 
import models

app = Flask(__name__)
app.config['SECRET_KEY'] = 'DEV'

twitter_blueprint = make_twitter_blueprint(api_key='', api_secret='')

github_blueprint = make_github_blueprint(client_id='', client_secret='')

DEBUG = True
PORT = int(os.environ.get('PORT', 5000))
#-------
#Login manager

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
# @app.before_request
# def before_request():
#     # """Connect to the DB before each request."""
#     g.db = models.DATABASE
#     g.db.connect()
#     g.user = current_user

# @app.after_request
# def after_request(response):
#     # """Close the database connection after each request."""
#     g.db.close()
#     return response
#-------
@app.route('/')
def index():
    if 'auth_token' in session:
        return redirect(url_for('profile'))
    else:
        return render_template('signin.html',title="Signin")

@app.route('/dashboard')
def dash(name=None):
    return render_template('dashboard.html', title="Dashboard", name=name)

@app.route('/siginin')
def signin(name=None):
    return render_template('signin.html', title='Sign-In', name=name)

#login
@app.route('/login', methods=['GET','POST'])
def login():
    form = forms.LoginForm()
    if form.validate_on_submit():
        try:
            user = models.User.get(models.User.email == form.email.data) # comparing the user email in the database to the one put in the form
        except models.DoesNotExist:
            flash("your email or password doesn't exist in our database")
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
    return index()

#register
@app.route('/register', methods=['GET', 'POST'])
def register():
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
            style = form.style.data
            )
        return redirect('/login')
    return render_template('register.html', title="Register", name=name)

#Profile
@app.route('/profile/')
@app.route('/profile', methods=['GET','POST'])
@login_required
def profile():
    return render_template('profile.html', user=current_user)

#edit profile
@app.route('/editProfile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = forms.UpdateUserForm()
    user = models.User.get(current_user.id)
    if form.validate_on_submit():
        user.height = form.height.data
        user.weight = form.height.data
        user.style = form.style.data
        user.save()
        flash('Profile has been updated')
        return redirect(url_for('profile'))

    return render_template('edit_profile.html', form = form)


#---------------------------------------------------------

# --------------------------------------------------------
# class User(db.Model):
#     __tablename__ = "users"
#     id = db.Column(db.Integer, primary_key=True)
#     username = db.Column(String(15), unique=True)
#     email = db.Column(db.String(120), unique=True)
#     password = db.Column(String)
#     age = db.Column(String)
#     location = db.Column(String)
#     height = db.Column(Integer)
#     weight = db.Column(Integer)
#     about = db.Column(String)
#     style= db.Column(String)

#     def __init__(self, email):
#         self.email = email

#     def __repr__(self):
#         return '<E-mail %r>' % self.email

if __name__ == '__main__':
    app.secret_key = os.urandom(12)
    app.run(debug=DEBUG, port=PORT)


