from flask import Flask, render_template, request, redirect, url_for, flash
from flask_user import current_user, login_required, roles_required, UserManager, UserMixin
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

with app.app_context():
    import models
    import routes
    import forms

class CustomUserManager(UserManager):

    def customize(self, app):

        # Configure customized forms
        self.RegisterFormClass = forms.CustomRegisterForm

user_manager = CustomUserManager(app, models.db, models.User)

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)
