from flask import Flask, g
from flask import render_template, flash, redirect, url_for, session, request, abort 
from flask import make_response as response
from forms import FightForm
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from flask_bcrypt import check_password_hash
from peewee import fn
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
            style = form.style.data
            )
        return redirect('/login')
    return render_template('register.html', title="Register", form=form)
#-----------------
# Profile
#-----------------
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

#--------------
# delete fight
#--------------

@app.route('/profile/<fightid>')
@login_required
def delete_fight(fightid):
    fight = models.Fight.get(fightid)
    fight.delete_instance()
    return redirect(url_for('profile'))

#--------------
# edit fight
#--------------
@app.route("/editfight/<fightid>", methods=['GET', 'POST'])
@login_required
def edit_fight(fightid):
    fight=models.Fight.get(models.Fight.id == fightid)
    form = forms.FightForm()
    if form.validate_on_submit():
        fight.name = form.name.data
        fight.description = form.description.data
        fight.save()
        fights = models.Fight.select().where(models.Fight.user == current_user.id)
        return render_template('profile.html', user=current_user, form=form, fights=fights)

    form.name.data = fight.name
    form.description.data = fight.description
    return render_template('edit_fight.html', user=current_user, form=form)

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
        return render_template('profile.html', user=current_user, form=form, fight=fights)
    return render_template('add_fight.html', user=current_user, form=form, fight=fights)

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
    models.initialize()
    app.secret_key = os.urandom(12)
    app.run(debug=DEBUG, port=PORT)


