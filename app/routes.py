from flask import render_template, url_for, flash, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from app import app, db
from app.forms import LoginForm,RegistrationForm
from app.models import User

@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")

@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('dashboard')
        return redirect(next_page)
    return render_template('login.html', form=form)

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/dashboard")
def dashboard():
    return render_template("dashboard.html")

@app.route('/dropoff')
def dropoff():
    return render_template("dropoff.html")

@app.route('/news')
def news():
    return render_template("news.html")

@app.route('/notifications')
def notifications():
    return render_template("notifications.html")

@app.route('/reedeem')
def reedeem():
    return render_template("reedeem.html")

@app.route('/rewards')
def rewards():
    return render_template("rewards.html")

@app.route('/schedule')
def schedule():
    return render_template("schedule.html")

@app.route('/settings')
def settings():
    return render_template("settings.html")

@app.route('/support')
def support():
    return render_template("support.html")

@app.route('/booking')
def booking():
    return render_template("booking.html")

@app.route('/user/<username>')
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    return render_template("user.html", user=user)