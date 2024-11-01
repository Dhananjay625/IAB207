from flask import Flask, render_template
from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Event, Booking, db, Comment
from .forms import TicketBookingForm, EventCreationForm
import random
from datetime import datetime

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def homepage():
    events = Event.query.all()  
    return render_template('homepage.html', events=events)


@main_bp.route('/cancel_event/<int:event_id>', methods=['POST'])
@login_required
def cancel_event(event_id):
    event = Event.query.get_or_404(event_id)

    if event.user_id != current_user.id:
        return redirect(url_for('main.event_details', event_id=event.id, message="You do not have permission to cancel this event."))

    db.session.delete(event)
    db.session.commit()
    return redirect(url_for('main.event_details', event_id=event.id, message="Event canceled successfully!"))


@main_bp.route('/edit_event/<int:event_id>', methods=['GET', 'POST'])
@login_required
def edit_event(event_id):
    event = Event.query.get_or_404(event_id)

    if event.user_id != current_user.id:
        return redirect(url_for('main.event_details', event_id=event.id, message="You do not have permission to edit this event."))

    form = EventCreationForm(obj=event)

    if request.method == 'POST' and form.validate_on_submit():
        event.name = form.name.data
        event.description = form.description.data
        event.date = form.date.data
        event.start_time = form.start_time.data
        event.end_time = form.end_time.data
        event.venue = form.venue.data
        event.price = form.price.data

        db.session.commit()
        return redirect(url_for('main.event_details', event_id=event.id, message="Event updated successfully!"))

    return render_template('ECreation.html', form=form, event=event)


@main_bp.route('/create_event', methods=['GET', 'POST'])
def create_event():
    form = EventCreationForm()

    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        description = form.description.data
        date = form.date.data
        start_time = form.start_time.data
        end_time = form.end_time.data
        venue = form.venue.data
        price = form.price.data

        print("Form data:", name, description, date, start_time, end_time, venue, price)  
        
        new_event = Event(
            name=name,
            description=description,
            date=date,
            start_time=start_time,
            end_time=end_time,
            venue=venue,
            status='Open',
            user_id=current_user.id
        )
        
        print("New event created:", new_event)

        try:
            db.session.add(new_event)
            db.session.commit()
        except Exception as e:
            db.session.rollback() 

        return redirect(url_for('main.homepage'))

    return render_template('ECreation.html', form=form)


@main_bp.route('/booking', methods=['GET', 'POST'])
@login_required 
def booking():
    events = Event.query.filter_by(status='Open').all()  
    
    if request.method == 'POST':
        event_id = request.form.get('selectEvent')
        quantity = request.form.get('ticketQuantity')
        
        if not event_id or not quantity:
            flash('Please select an event and specify the number of tickets.', 'danger')
            return redirect(url_for('main.booking'))
        
        try:
            quantity = int(quantity) 
            price = 100 * quantity 
            
            new_booking = Booking(quantity=quantity, price=price, user_id=current_user.id, event_id=event_id)
            db.session.add(new_booking)
            db.session.commit()
            
            flash('Booking confirmed!', 'success')
            return redirect(url_for('main.homepage'))
        
        except ValueError:
            flash('Invalid input. Please enter a valid number for tickets.', 'danger')
            return redirect(url_for('main.booking'))
    
    return render_template('booking.html', events=events)

@main_bp.route('/event/<int:event_id>')
def event_details(event_id):
    event = Event.query.get_or_404(event_id)
    comments = Comment.query.filter_by(event_id=event_id).all()
    message = request.args.get('message')  
    edit_mode = request.args.get('edit') == 'true' 
    return render_template('EDetails.html', event=event, comments=comments, message=message)


@main_bp.route('/booking_history')
@login_required
def booking_history():
    bookings = Booking.query.filter_by(user_id=current_user.id).all()
    return render_template('BHistory.html', bookings=bookings)


@main_bp.route('/trigger-500')
def trigger_500():
    return 1 / 0
