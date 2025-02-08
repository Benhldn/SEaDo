import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from src.database import init_db, db_session, Base 
from src.models import Ticket, User 

class TestDatabase(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.engine = create_engine('sqlite:///:memory:')  
        cls.db_session = scoped_session(sessionmaker(autocommit=False,
                                                     autoflush=False,
                                                     bind=cls.engine))
        Base.query = cls.db_session.query_property()

        Base.metadata.create_all(bind=cls.engine)

    def setUp(self):
        # Clear the session before each test
        self.db_session.remove()

    def test_init_db(self):
        # Call init_db to populate the database
        init_db()

        # Check if Ticket is populated
        ticket = self.db_session.get(Ticket, 1)
        self.assertIsNotNone(ticket)
        self.assertEqual(ticket.email, "example@gmail.com")
        self.assertEqual(ticket.title, "Ticket_Test")
        self.assertEqual(ticket.description, "This is a test")
        self.assertEqual(ticket.date, "21-01-01")

        # Check if User is populated
        user = self.db_session.get(User, 1)
        self.assertIsNotNone(user)
        self.assertEqual(user.email, "admin@email.com")
        self.assertEqual(user.password, "Admin")
        self.assertTrue(user.admin)
        print(user.admin)

    @classmethod
    def tearDownClass(cls):
        # Remove the session and close the engine
        cls.db_session.remove()
        cls.engine.dispose()

if __name__ == '__main__':
    unittest.main()
