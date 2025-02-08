import unittest
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from src.database import Base, init_db, populate_tickets, populate_users  
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
       
        self._old_db_session = init_db.__globals__['db_session'] 
        init_db.__globals__['db_session'] = self.db_session 

    def tearDown(self):
    
        self.db_session.remove()  
        init_db.__globals__['db_session'] = self._old_db_session  

    def test_populate_tickets(self):
        populate_tickets()


        ticket = self.db_session.get(Ticket, 1)
        self.assertIsNotNone(ticket, "Ticket should be created by populate_tickets")
        self.assertEqual(ticket.email, "example@gmail.com")
        self.assertEqual(ticket.title, "Ticket_Test")
        self.assertEqual(ticket.description, "This is a test")
        self.assertEqual(ticket.date, "21-01-01")

    def test_init_db(self):
        init_db()

        ticket = self.db_session.get(Ticket, 1)
        self.assertIsNotNone(ticket, "Ticket should be created by init_db")
        self.assertEqual(ticket.email, "example@gmail.com")
        self.assertEqual(ticket.title, "Ticket_Test")
        self.assertEqual(ticket.description, "This is a test")
        self.assertEqual(ticket.date, "21-01-01")

        user = self.db_session.get(User, 1)
        self.assertIsNotNone(user, "User should be created by init_db")
        self.assertEqual(user.email, "admin@email.com")
        self.assertEqual(user.password, "Admin")
        self.assertTrue(user.admin)

    @classmethod
    def tearDownClass(cls):
        cls.db_session.remove()
        cls.engine.dispose()

if __name__ == '__main__':
    unittest.main()


