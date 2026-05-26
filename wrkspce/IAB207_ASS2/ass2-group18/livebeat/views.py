from flask import Blueprint, render_template, redirect, url_for, flash, request, abort, current_app
from flask_login import login_required, current_user
from datetime import datetime
import os
from werkzeug.utils import secure_filename

from . import db
from .models import Event, Booking, Comment
from .forms import EventForm, BookingForm


main_bp = Blueprint("main", __name__)


@main_bp.app_context_processor
def inject_has_created_events():
    has_created_events = False
    if current_user.is_authenticated:
        has_created_events = Event.query.filter_by(user_id=current_user.id).first() is not None
    return {"has_created_events": has_created_events}

#US14
def mark_past_events_inactive():
    now = datetime.now()
    past_open_events = Event.query.filter( Event.date < now, Event.status == "Open").all()

    if past_open_events:
        for event in past_open_events:
            event.status = "Inactive"
        db.session.commit()

@main_bp.route("/")
def index():
    mark_past_events_inactive()
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
    if event.status not in ("Inactive", "Sold Out", "Cancelled") and event.date < datetime.now():
        event.status = "Inactive"
        db.session.commit()
    comments = Comment.query.filter_by(event_id=event.id).order_by(Comment.date.desc()).all()
    booking_form = BookingForm()

    return render_template(
        "event-details.html",
        event=event,
        comments=comments,
        booking_form=booking_form,
    )


@main_bp.route("/create-event", methods=["GET", "POST"])
@login_required
def create_event():
    form = EventForm()

    if form.validate_on_submit():
        event_datetime = datetime.combine(form.date.data, form.time.data)
        end_datetime = datetime.combine(form.date.data, form.end_time.data) if form.end_time.data else None

        # Handle image upload
        image_filename = "concert1.jpg"
        if form.image.data and hasattr(form.image.data, "filename") and form.image.data.filename:
            f = form.image.data
            filename = secure_filename(f.filename)
            upload_folder = os.path.join(current_app.root_path, 'static', 'images')
            f.save(os.path.join(upload_folder, filename))
            image_filename = filename

        event = Event(
            title=form.title.data,
            artist=form.artist.data,
            description=form.description.data,
            category=form.category.data,
            capacity=form.capacity.data,
            date=event_datetime,
            end_time=end_datetime,
            venue_name=form.venue_name.data,
            venue_address=form.venue_address.data,
            ticket_price=form.ticket_price.data,
            ticket_type=form.ticket_type.data,
            acknowledgement=form.acknowledgement.data,
            user_id=current_user.id,
            status="Open",
            image=image_filename,
        )

        db.session.add(event)
        db.session.commit()

        flash("Event created successfully.")
        return redirect(url_for("main.event_details", event_id=event.id))

    return render_template("create-event.html", form=form)


@main_bp.route("/events/<int:event_id>/edit", methods=["GET", "POST"])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)

    # Only the owner can edit
    if event.user_id != current_user.id:
        abort(403)

    form = EventForm(obj=event)

    if form.validate_on_submit():
        updated_start_datetime = datetime.combine(form.date.data, form.time.data)
        event.title = form.title.data
        event.artist = form.artist.data
        event.description = form.description.data
        event.category = form.category.data
        event.capacity = form.capacity.data
        event.date = updated_start_datetime
        event.end_time = datetime.combine(form.date.data, form.end_time.data) if form.end_time.data else None
        event.venue_name = form.venue_name.data
        event.venue_address = form.venue_address.data
        event.ticket_price = form.ticket_price.data
        event.ticket_type = form.ticket_type.data
        # Update image only if a new one was uploaded
        if form.image.data and hasattr(form.image.data, "filename") and form.image.data.filename:
            f = form.image.data
            filename = secure_filename(f.filename)
            upload_folder = os.path.join(current_app.root_path, 'static', 'images')
            f.save(os.path.join(upload_folder, filename))
            event.image = filename
        event.acknowledgement = form.acknowledgement.data

        # Reactivate only when an inactive event is moved to the future.
        if event.status == "Inactive" and updated_start_datetime >= datetime.now():
            event.status = "Open"

        # Reopen sold-out events when tickets are added back.
        if event.status and event.status.strip().lower() == "sold out" and event.capacity > 0:
            event.status = "Open"

        db.session.commit()
        flash("Event updated successfully.")
        return redirect(url_for("main.event_details", event_id=event.id))

    # Pre-fill date and time fields from existing event
    if request.method == "GET":
        form.date.data = event.date.date()
        form.time.data = event.date.time()
        if event.end_time:
            form.end_time.data = event.end_time.time()

    return render_template("create-event.html", form=form, editing=True, event=event)


@main_bp.route("/events/<int:event_id>/cancel", methods=["POST"])
@login_required
def cancel_event(event_id):
    event = Event.query.get_or_404(event_id)

    if event.user_id != current_user.id:
        abort(403)

    event.status = "Cancelled"
    db.session.commit()
    flash("Event has been cancelled.")
    return redirect(url_for("main.event_details", event_id=event.id))


@main_bp.route("/my-events")
@login_required
def my_events():
    events = Event.query.filter_by(user_id=current_user.id).order_by(Event.date.desc()).all()
    return render_template("my-events.html", events=events)


@main_bp.route("/booking-history")
@login_required
def booking_history():
    bookings = Booking.query.filter_by(user_id=current_user.id).order_by(Booking.date_booked.desc()).all()
    return render_template("booking-history.html", bookings=bookings)


@main_bp.route("/events/<int:event_id>/book", methods=["POST"])
@login_required
def book_event(event_id):
    event = Event.query.get_or_404(event_id)
    form = BookingForm()

    if not form.validate_on_submit():
        flash("Please enter a valid ticket quantity.")
        return redirect(url_for("main.event_details", event_id=event.id))

    if event.status != "Open":
        flash("This event is not available for booking.")
        return redirect(url_for("main.event_details", event_id=event.id))

    quantity = form.ticket_quantity.data

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
