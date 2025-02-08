import pytest
import uuid
from flask import Flask
from flask import Blueprint, render_template, redirect, url_for, request, flash
from src import create_app, database
from src.models import User
from flask_login import current_user

@pytest.fixture
def app():
    app = create_app()
    app.config.update({
        "TESTING": True,
        "SQLALCHEMY_DATABASE_URI": "sqlite:///test.db",
        "SECRET_KEY": "secret-key"
    })

    with app.app_context():
        # Initialize the database and create tables
        database.init_db()

    yield app

    with app.app_context():
        # Clean up database after each test
        database.db_session.remove()

@pytest.fixture
def client(app):
    return app.test_client()

@pytest.fixture
def runner(app):
    return app.test_cli_runner()

# Generate a unique email for each test
def generate_unique_email():
    return f"test_{uuid.uuid4()}@example.com"

def test_login_page(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data

def test_success_page(client, app):
    response = client.get('/success')
    assert response.status_code == 302  # Redirect to login page when not logged in

def test_signUp_page(client):
    response = client.get('/signUp')
    assert response.status_code == 200
    assert b'Sign Up' in response.data

def test_loginPost(client, app):
    # Generate a unique email to avoid conflicts with existing data
    unique_email = generate_unique_email()

    # Create a new user directly in the test database
    with app.app_context():
        new_user = User(email=unique_email, password='password')
        database.db_session.add(new_user)
        database.db_session.commit()

    # Simulate login POST request with the unique email
    response = client.post('/login', data={
        'inputEmail': unique_email,
        'inputPassword': 'password'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert current_user.is_authenticated

def test_signUpPost(client, app):
    # Generate a unique email for this test
    unique_email = generate_unique_email()

    # Test the user signup process
    response = client.post('/signUp', data={
        'inputEmail': unique_email,
        'inputPassword': 'newpassword'
    }, follow_redirects=True)

    assert response.status_code == 200

    with app.app_context():
        # Verify that the new user was added to the database
        user = User.query.filter_by(email=unique_email).first()
        assert user is not None

def test_logout(client):
    response = client.get('/logout', follow_redirects=True)
    assert response.status_code == 200