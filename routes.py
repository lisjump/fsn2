from flask import Flask, render_template, request, redirect, url_for, flash
from flask_user import login_required, UserManager, UserMixin, current_user
import models
import forms
import utils.errors as errors
from flask import current_app as app
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, date

db = SQLAlchemy(app)


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    return render_template(
        'index.html',)

@app.route('/register', methods=['GET', 'POST'])
@login_required
def register(houseid = None):
    if "admin" in [i.name for i in current_user.roles] and request.args.get('householdid'):
        houseid = request.args.get('householdid')
    elif current_user.households:
        houseid = current_user.households.pop().id

    # raise(AttributeError)
    if houseid:
        household = db.session.query(models.Household).filter_by(id = houseid).first()
    else:
        household = models.Household()

    if not request.method == 'POST':
        form = forms.RegistrationForm(obj = household)
        if houseid:
            form.populate_obj(household)
        for i in range(0, 10):
          form.users.append_entry()

    else:

        form  = forms.RegistrationForm(request.form, obj=household)
        if form.validate():
            form.populate_obj(household)
            i = 0

            if household.email == "":
                household.email = None

            while i < len(household.users):
                user = household.users[i]
                if not (user.first or user.last or user.email):
                    household.users.remove(user)
                    db.session.flush()
                    if user.id:
                        db.session.delete(user)
                else:
                    i = i + 1

            if not household.id:
                db.session.add(household)

            db.session.commit()
            return redirect(url_for('index'))
        else:
            errors.flash_errors(form)


    return render_template('register.html', form = form, errors = form.errors, currentyear = datetime.now().year)

@app.route('/usersettings', methods=['GET', 'POST'])
@login_required
def usersettings():
    return render_template('usersettings.html')
