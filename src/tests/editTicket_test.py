import unittest
from flask import Flask
from src.database import edit, db_session  
from src.models import Ticket, User  
from flask.testing import FlaskClient
from unittest.mock import patch

class TestEditTicket(unittest.TestCase):
    def setUp(self):
        self.app = Flask(__name__)
        self.app.register_blueprint(edit)
        self.client = self.app.test_client()
        self.app.config['TESTING'] = True
        self.app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        with self.app.app_context():
            db_session.begin()
            Ticket.metadata.create_all(bind=db_session.bind)
            User.metadata.create_all(bind=db_session.bind)
            db_session.commit()

    def tearDown(self):
        db_session.remove()

    @patch('your_module.login_required', lambda x: x)  
    def test_ticket_edit_get(self):
        with self.app.app_context():
            ticket = Ticket(id=1, title="Test Ticket", description="Test Description")
            db_session.add(ticket)
            db_session.commit()

        response = self.client.get("/editTicket/1")

        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Test Ticket", response.data)
        self.assertIn(b"Test Description", response.data)

    @patch('your_module.login_required', lambda x: x)
    def test_ticket_edit_post(self):
        with self.app.app_context():
            ticket = Ticket(id=1, title="Old Title", description="Old Description")
            db_session.add(ticket)
            db_session.commit()

        response = self.client.post("/editTicket/1", data={
            'inputTitle': 'New Title',
            'inputDescription': 'New Description'
        }, follow_redirects=True)

        self.assertEqual(response.status_code, 200)

        with self.app.app_context():
            updated_ticket = db_session.query(Ticket).filter_by(id=1).first()
            self.assertEqual(updated_ticket.title, "New Title")
            self.assertEqual(updated_ticket.description, "New Description")

if __name__ == '__main__':
    unittest.main()
