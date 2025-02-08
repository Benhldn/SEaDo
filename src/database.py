from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker, declarative_base

engine = create_engine('sqlite:///instance/db.sqlite')
db_session = scoped_session(sessionmaker(autocommit=False,
                                         autoflush=False,
                                         bind=engine))
Base = declarative_base()
Base.query = db_session.query_property()


def init_db():
   
    from .models import Ticket, User
    Base.metadata.create_all(bind=engine)

    checkTickets = db_session.get(Ticket, 1)
    if not checkTickets:
        populate_tickets()

    checkUsers = db_session.get(User, 1)
    if not checkUsers:
        populate_users()


def populate_tickets():
    from .models import Ticket

    db_session.add_all(
        [
            Ticket(id="1", email="example@gmail.com", title="Ticket 1", description="This is a test", date="21-01-01"),
            Ticket(id="2", email="example@gmail.com", title="Ticket 2", description="This is a test", date="21-01-01"),
            Ticket(id="3", email="example@gmail.com", title="Ticket 3", description="This is a test", date="21-01-01"),
            Ticket(id="4", email="example@gmail.com", title="Ticket 4", description="This is a test", date="21-01-01"),
            Ticket(id="5", email="example@gmail.com", title="Ticket 5", description="This is a test", date="21-01-01"),
            Ticket(id="6", email="example@gmail.com", title="Ticket 6", description="This is a test", date="21-01-01"),
            Ticket(id="7", email="example@gmail.com", title="Ticket 7", description="This is a test", date="21-01-01"),
            Ticket(id="8", email="example@gmail.com", title="Ticket 8", description="This is a test", date="21-01-01"),
            Ticket(id="9", email="example@gmail.com", title="Ticket 9", description="This is a test", date="21-01-01"),
            Ticket(id="10", email="example@gmail.com", title="Ticket 10", description="This is a test", date="21-01-01"),
        ]
    )
    db_session.commit()

def populate_users():
    from .models import User

    db_session.add_all(
        [
            User(id="1", email="admin@email.com", password="Admin", admin=True)
        ]
    )
    db_session.commit()
