from flask import render_template, redirect, url_for, flash
from manager.models import  User, Client, Databases
from manager.forms import RegisterForm, LoginForm, AddDBForm
from manager import db
from manager import app
from manager.migrations import start_migrations
from flask_login import login_user, logout_user, login_required

@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')

@app.route('/add_database', methods=['GET', 'POST'])
@login_required
def configurations_page():
    form = AddDBForm()
    items = Databases.query.filter_by(connection_test_result=False)
    if form.validate_on_submit():
        database_to_add = Databases(
            name = form.name.data,
            db_type = form.type.data,
            db_uri = form.uri.data,
            db_username = form.username.data,
            db_password = form.password.data,
            connection_test_result= False,
        )
        
        db.session.add(database_to_add)
        db.session.commit()
            
        flash(f'Success! Added Database: {form.name.data}', category='success')
        return redirect(url_for('configurations_page'))
        
    return render_template('configurations.html', form=form, items=items)

@app.route('/register', methods=['GET', 'POST'])
def register_page():
    form = RegisterForm()
    if form.validate_on_submit():
        user_to_create = Client(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)
        db.session.add(user_to_create)
        db.session.commit()
        login_user(user_to_create)
        flash(f"Account created successfully! You are now logged in as {user_to_create.username}", category='success')
        return redirect(url_for('configurations_page'))
    if form.errors != {}: #If there are not errors from the validations
        for err_msg in form.errors.values():
            flash(f'There was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()
    if form.validate_on_submit():
        attempted_user = User.query.filter_by(username=form.username.data).first()
        if attempted_user and attempted_user.check_password_correction(
                attempted_password=form.password.data
        ):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('configurations_page'))
        else:
            flash('Username and password are not matching! Please try again', category='danger')

    return render_template('login.html', form=form)

@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for("home_page"))

@app.route('/logs', methods=['GET', 'POST'])
@login_required
def monitor_logs():
    start_migrations()
    return "Started"










