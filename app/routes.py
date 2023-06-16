from flask import render_template, url_for, flash, redirect, request
from flask_login import current_user, login_user, logout_user, login_required
from werkzeug.urls import url_parse

from random import sample

from app import app, db
from app.forms import LoginForm,RegistrationForm, HouseForm
from app.forms import EditProfileForm
from app.models import User, House

@app.route('/index')    
def index():
    return render_template('base.html')

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
    return render_template('login.html', form=form, title="Login")

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', form=form, title="Register")

@app.route('/')
@app.route('/dashboard')
def dashboard():
    return render_template('dash.html', title='Dashboard', titles=sample(House.query.all(), 1))

@app.route('/add', methods=['GET', 'POST'])
@login_required
def add():
    form = HouseForm()
    if form.validate_on_submit():
        house = House(name=form.name.data, address=form.address.data, remarks=form.remarks.data, rent=int(form.rent.data),\
                      number_of_rooms=form.number_of_rooms.data, owner=current_user.id, caution_deposit=form.caution_deposit.data)
        db.session.add(house)
        db.session.commit()
        flash("House added")
        return redirect(url_for('login'))
    return render_template('add.html', form=form, title="Add Books")

@app.route('/house/<id>')
def house(id):
    house = House.query.filter_by(id=id).first_or_404()
    return render_template('house.html', house=house, title='View House')

@app.route('/user/<id>')
def user(id):
    user = User.query.filter_by(id=id).first_or_404()
    house_list = House.query.filter_by(owner=user.id)
    return render_template('user.html', user=user, house_list=house_list, title="%s's profile" % user.username)

@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def settings():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash('Your changes have been saved.')
        return redirect(url_for('settings'))
    elif request.method == 'GET':
        form.username.data = current_user.username
    return render_template('settings.html', title='Edit Profile', form=form)

@app.route('/delete', methods=["GET"])
def delete():
    u = User.query.filter_by(id=current_user.id).first_or_404()
    db.session.delete(u)
    db.session.commit()
    return redirect(url_for('logout'))