from flask import Blueprint, render_template, redirect, url_for, request, flash
from flask_login import login_required, current_user
from .models import Ticket, User
from .database import db_session
from .auth import login_required

create = Blueprint('create', __name__)

@create.route('/createTicket', methods=['GET', 'POST'])
@login_required
def ticketPOST():

    
    title = request.form.get('inputTitle')
    email = current_user.email
    description = request.form.get('inputDescription')
    date = request.form.get('inputDate')
    
    print(title, email, description, date)

    new_ticket = Ticket(title=title, email=email, description=description, date=date)

    db_session.add(new_ticket)
    db_session.commit()
    print(new_ticket)

    return redirect(url_for('main.home'))