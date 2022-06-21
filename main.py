from flask import Flask, escape, request, render_template, url_for
from forms import RegistrationForm, LoginForm

# Want to use url_for for links within project

# "name" is same as "self"?
app = Flask(__name__)

app.config['SECRET_KEY'] = 'aa5357f134362045710b1f5bad84a4c5'

# Have to set an environment variable to the file that we want to be the flask application for this
# We did `export FLASK_APP=main.py` --> new command line (green arrow)
# then we enter the command `flask run`
# have to exit out and do this again UNTIL
# Enter the command `export FLASK_DEBUG=1` and this makes it so we don't have to restart the server every time


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
    return render_template('register.html', title='Register', form=form)


@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Login', form=form)

# This is only true if we run this script directly, if we run this with Python itself
# Run the command `Python main.py`
if __name__ == '__main__':
    app.run(debug=True)


