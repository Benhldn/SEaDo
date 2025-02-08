import unittest
from unittest.mock import patch
from flask import Flask
from flask_login import LoginManager, UserMixin
from .createTicket import create  # Replace with your actual import

class User(UserMixin):
    def __init__(self, email):
        self.email = email

class Ticket:
    def __init__(self, title, email, description, date):
        self.title = title
        self.email = email
        self.description = description
        self.date = date

# Mocking the database session for testing
class MockDBSession:
    tickets = []

    @classmethod
    def add(cls, ticket):
        cls.tickets.append(ticket)

    @classmethod
    def commit(cls):
        pass

class CreateTicketTests(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(create)
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing
        self.client = self.app.test_client()

        self.login_manager = LoginManager()
        self.login_manager.init_app(self.app)

        @self.login_manager.user_loader
        def load_user(user_id):
            return User("test@example.com")

    @patch('your_application.current_user', new_callable=lambda: User("test@example.com"))
    @patch('your_application.db_session', new_callable=lambda: MockDBSession)
    def test_create_ticket(self, mock_db_session):
        response = self.client.post('/createTicket', data={
            'inputTitle': 'Test Ticket',
            'inputDescription': 'This is a test description',
            'inputDate': '2024-09-23'
        })

        self.assertEqual(response.status_code, 302)  # Check for redirect
        self.assertEqual(len(mock_db_session.tickets), 1)  # Check ticket was added
        ticket = mock_db_session.tickets[0]
        self.assertEqual(ticket.title, 'Test Ticket')
        self.assertEqual(ticket.email, 'test@example.com')
        self.assertEqual(ticket.description, 'This is a test description')
        self.assertEqual(ticket.date, '2024-09-23')

if __name__ == '__main__':
    unittest.main()
