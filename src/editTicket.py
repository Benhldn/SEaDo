from flask import Blueprint, redirect, render_template, url_for, request
from .models import Ticket
from .database import db_session
from .auth import login_required

edit = Blueprint('edit', __name__)

@edit.route("/editTicket/<int:ticket_id>", methods=["GET", "POST"])
@login_required
def ticketEdit(ticket_id):
    original_ticket = Ticket.query.filter_by(id=ticket_id).first()

    if not original_ticket:
        return redirect(url_for("main.home"))

    if request.method == "GET":
        return render_template("editTicket.html", ticket=original_ticket)

    new_title = request.form.get("inputTitle")
    new_description = request.form.get("inputDescription")

    original_ticket.title = new_title
    original_ticket.description = new_description

    db_session.commit()

    return redirect(url_for("main.home"))