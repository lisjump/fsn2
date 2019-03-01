import datetime
import google.oauth2.id_token
from flask import Flask, render_template, request, redirect, url_for, flash
from google.auth.transport import requests
from google.cloud import datastore
from keys import *
from flask_login import LoginManager, login_required, login_user, logout_user, UserMixin, current_user
from urllib.parse import urlparse, urljoin
from config import Config
from forms import *
from flask_sqlalchemy import SQLAlchemy

# datastore_client = datastore.Client()

#  --------  INITIALIZING AND UTILITIES  --------

firebase_request_adapter = requests.Request()

app = Flask(__name__)
app.config.from_object(Config)
login = LoginManager(app)
login.login_view = 'login'
db = SQLAlchemy(app)
from models import *
from routes import *

def is_safe_url(target):
    ref_url = urlparse(request.host_url)
    test_url = urlparse(urljoin(request.host_url, target))
    return test_url.scheme in ('http', 'https') and \
           ref_url.netloc == test_url.netloc

#  --------  SESSION MANAGEMENT  --------
@login.user_loader
def load_user(id):
    return User.query.get(int(id))


#  --------  SCHTUFF  --------


# @app.route('/login', methods=['GET', 'POST'])
# def login():
    # Verify Firebase auth.
    # id_token = request.cookies.get("token")
    #
    # if id_token:
    #     try:
    #         # Verify the token against the Firebase Auth API.
    #         claims = google.oauth2.id_token.verify_firebase_token(
    #             id_token, firebase_request_adapter)
    #         user = User(id = id_token)
    #         login_user(user)
    #         print("hello")
    #     except ValueError as exc:
    #         # This will be raised if the token is expired or any other
    #         # verification checks fail.
    #         error_message = str(exc)
    #         return redirect(url_for('login'))
    #
    #     next = request.args.get('next')
    #     # is_safe_url should check if the url is safe for redirects.
    #     # See http://flask.pocoo.org/snippets/62/ for an example.
    #     if not is_safe_url(next):
    #         return flask.abort(400)
    #     else:
    #         return redirect(next)
    # return render_template('login.html', title='Sign In', form=form)

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
@login_required
def index():
    user = User()
    login_user(user)

    return render_template(
        'index.html',)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
