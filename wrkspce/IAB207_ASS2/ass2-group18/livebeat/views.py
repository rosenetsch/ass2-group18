from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from datetime import datetime

from . import db
from .models import Event, Booking, Comment
from .forms import EventForm


main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index():
    selected_category = request.args.get("category", "all")

    query = Event.query.order_by(Event.date.asc())

    if selected_category != "all":
        query = query.filter(Event.category.ilike(selected_category))

    events = query.all()

    categories = ["all", "rock", "pop", "jazz", "rnb", "soul", "other"]

    return render_template(
        "index.html",
        events=events,
        categories=categories,
        selected_category=selected_category,
    )


@main_bp.route("/events/<int:event_id>", methods=["GET", "POST"])
def event_details(event_id):
    event = Event.query.get_or_404(event_id)
    comments = Comment.query.filter_by(event_id=event.id).order_by(Comment.date.desc()).all()

    return render_template(
        "event-details.html",
        event=event,
        comments=comments,
    )


@main_bp.route("/create-event", methods=["GET", "POST"])
@login_required
def create_event():
    form = EventForm()

    if form.errors:
        print("CREATE EVENT FORM ERRORS:", form.errors)

    if form.validate_on_submit():
        event_datetime = datetime.combine(form.date.data, form.time.data)

        event = Event(
            title=form.title.data,
            artist=form.artist.data,
            description=form.description.data,
            category=form.category.data,
            capacity=form.capacity.data,
            date=event_datetime,
            venue_name=form.venue_name.data,
            venue_address=form.venue_address.data,
            ticket_price=form.ticket_price.data,
            acknowledgement=form.acknowledgement.data,
            user_id=current_user.id,
            status="Open",
            image="concert1.jpg",
        )

        db.session.add(event)
        db.session.commit()

        flash("Event created successfully.")
        return redirect(url_for("main.event_details", event_id=event.id))

    return render_template("create-event.html", form=form)


@main_bp.route("/booking-history")
@login_required
def booking_history():
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.date_booked.desc()).all()
    return render_template("booking-history.html", bookings=bookings)


@main_bp.route("/events/<int:event_id>/book", methods=["POST"])
@login_required
def book_event(event_id):
    event = Event.query.get_or_404(event_id)

    if event.status != "Open":
        flash("This event is not available for booking.")
        return redirect(url_for("main.event_details", event_id=event.id))

    try:
        quantity = int(request.form.get("ticket_quantity", 1))
    except (TypeError, ValueError):
        flash("Please enter a valid ticket quantity.")
        return redirect(url_for("main.event_details", event_id=event.id))

    if quantity < 1:
        flash("Ticket quantity must be at least 1.")
        return redirect(url_for("main.event_details", event_id=event.id))

    if event.capacity <= 0:
        event.status = "Sold Out"
        db.session.commit()
        flash("This event is sold out.")
        return redirect(url_for("main.event_details", event_id=event.id))

    if quantity > event.capacity:
        flash(f"Only {event.capacity} tickets are available.")
        return redirect(url_for("main.event_details", event_id=event.id))

    booking = Booking(
        ticket_quantity=quantity,
        ticket_price=event.ticket_price,
        user_id=current_user.id,
        event_id=event.id,
    )

    event.capacity -= quantity

    if event.capacity == 0:
        event.status = "Sold Out"

    db.session.add(booking)
    db.session.commit()

    flash(f"Booking confirmed. Your order ID is LB{booking.id}.")
    return redirect(url_for("main.booking_history"))


@main_bp.route("/events/<int:event_id>/comment", methods=["POST"])
@login_required
def add_comment(event_id):
    event = Event.query.get_or_404(event_id)
    text = request.form.get("comment_text", "").strip()

    if text:
        comment = Comment(
            text=text,
            user_id=current_user.id,
            event_id=event.id,
        )

        db.session.add(comment)
        db.session.commit()

        flash("Comment added.")
    else:
        flash("Comment cannot be empty.")

    return redirect(url_for("main.event_details", event_id=event.id))
