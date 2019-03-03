from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import login_user, logout_user, current_user
from flask_user import login_required, UserManager, UserMixin
import models
import forms
import utilities
from flask import current_app as app


# @login.user_loader
# def load_user(id):
#     return models.User.query.get(int(id))

@app.route('/logins', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = forms.LoginForm()
    if form.validate_on_submit():
        user = models.User.query.filter_by(id=int(form.username.data)).first()
        user.username = "joe"
        if user is None:
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next = request.args.get('next')
        if not next or not utilities.is_safe_url(next):
            next = url_for('index')
        return redirect(next)
    return render_template('login.html', form=form)

# @app.route('/logout')
# def logout():
#     logout_user()
#     return redirect(url_for('index'))

@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():

    return render_template(
        'index.html',)
