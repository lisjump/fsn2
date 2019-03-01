from flask_login import current_user, login_user
from models import *

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(id=int(form.username.data)).first()
        user.username = "joe"
        if user is None:
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next = request.args.get('next')
        if not next or urlparse(next).netloc != '' or not is_safe_url(next):
            next = url_for('index')
        return redirect(next)
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))
