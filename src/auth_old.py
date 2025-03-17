from flask import Blueprint, render_template, redirect, url_for, request, flash
from .models import User
from .database import db_session
from flask_login import login_user, login_required, logout_user
from sqlalchemy.exc import NoResultFound

auth = Blueprint('auth', __name__)

@auth.route('/login')
def login():
    return render_template('login.html')

@auth.route('/login', methods=['POST'])
def loginPost():

    email = request.form.get('inputEmail')
    password = request.form.get('inputPassword')
    
    print(email, password)

    try:
        user = db_session.query(User).filter(User.email == email).one()
    except NoResultFound:
        return redirect(url_for('auth.login'))
    
    print(user)

    actualPassword = db_session.query(User.password).filter_by(email=email).first()[0]
    if password != actualPassword:
        return redirect(url_for('auth.login'))
    else:
        login_user(user)
        return redirect(url_for('main.home'))
    


@auth.route('/success')
@login_required
def success():
    return render_template('home.html')

    
@auth.route('/signUp')
def signUp():
    return render_template('signUp.html')


@auth.route('/signUp', methods=['GET', 'POST'])
def signUpPost():

    email = request.form.get('inputEmail')
    password = request.form.get('inputPassword')

    user = db_session.query(User).filter(User.email == email).one_or_none() 

    if user:
        flash('User already exists, try again.')
        return redirect(url_for('auth.signUp'))
    else:

        new_user = User(email=email, password=password)

        db_session.add(new_user)
        db_session.commit()
        print(new_user)

    return redirect(url_for('auth.login'))


@auth.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("auth.login"))



