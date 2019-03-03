import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin

from config import Config
from forms import *

app = Flask(__name__)
app.config.from_object(Config)

with app.app_context():
    import models
    import routes

user_manager = UserManager(app, models.db, models.User)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
