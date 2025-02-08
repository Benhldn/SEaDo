from flask import Blueprint, redirect, render_template, url_for
from flask_login import login_required, current_user
from .models import Ticket
from .database import db_session


main = Blueprint('main', __name__)

@main.route('/')
@login_required
def home():
    return render_template('home.html', tickets=Ticket.query.all())

@main.route('/createTicket')
@login_required
def createTicket():
    return render_template('createTicket.html')

@main.route('/editTicket')
@login_required
def editTicket():
    return render_template('editTicket.html')

@main.route("/deleteTicket/<int:ticket_id>", methods=["GET", "POST"])
@login_required
def deleteTicket(ticket_id):
    if current_user.admin == True:
        Ticket.query.filter_by(id=ticket_id).delete()

        db_session.commit()

    return redirect(url_for("main.home"))


