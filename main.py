from flask import Flask, escape, request, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

# Want to use url_for for links within project

# "name" is same as "self"?
app = Flask(__name__)
app.config['SECRET_KEY'] = 'aa5357f134362045710b1f5bad84a4c5'
# Setting the location of the database we need to use a configuration
# the '///' is the relative path from the file
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
# Database structure are classes and are referred to as models

# Have to set an environment variable to the file that we want to be the flask application for this
# We did `export FLASK_APP=main.py` --> new command line (green arrow)
# then we enter the command `flask run`
# have to exit out and do this again UNTIL
# Enter the command `export FLASK_DEBUG=1` and this makes it so we don't have to restart the server every time
# entering control+C will stop the development server from running


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # lazy argument as true will load the data as necessary in one go
    # Helps us get all the stuff from a user without any extra code
    posts = db.relationship('Post', backref='author', lazy=True)

    # How our object is printed when it is printed out
    # Referred to as Dunder Methods (double underscore method)
    def __repr__(self):
        return f"User('{self.username}', '{self.image}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    # utc times --> pass in the function without the () so it does not pass in the actual current time
    # but rather passes in the function
    # Always want to use UTC times when passing times into a database so they are consistent
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    # use the lowercase 'user' in this case cause we are referencing the post model
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"User('{self.username}', '{self.date_posted}')"


posts = [
    {
        'author': 'Jamie Flynt',
        'title': 'Blog Post 1',
        'content': 'First Post Content',
        'date_posted': 'June 8, 2022',
    },
    {
        'author': 'Amanda Wood',
        'title': 'Blog Post 2',
        'content': 'Second Post Content',
        'date_posted': 'June 9, 2022',
    }
]


# Both these routes are handled by the same function, i.e. hello()
@app.route('/')
@app.route('/home')
def hello():
    # import the render_template() function from Flask
    return render_template("home.html", posts=posts)


@app.route('/about')
def about():
    return render_template("about.html", title="About")


@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        # Second argument in the flash method is the style (in this case Bootstrap)
        flash(f'Account created for {form.username.data}!', 'success')
        # note the url_for method is taking the name of the function in the redirect
        return redirect(url_for('hello'))
    return render_template('register.html', title='Register', form=form)


@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        # Test to see if login is successful or no, functionality not complete
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':
            flash('You have been logged in!', 'success')
            return redirect(url_for('hello'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html', title='Login', form=form)

# This is only true if we run this script directly, if we run this with Python itself
# Run the command `Python main.py`


if __name__ == '__main__':
    app.run(debug=True)


# ORM (Object Relational Mapper) --> organizes database in an easy to use OOP way
# SQL Lite Database