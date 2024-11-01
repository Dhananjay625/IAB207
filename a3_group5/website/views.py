from flask import Flask, render_template
from flask import Blueprint, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Event, Booking, db
from .forms import TicketBookingForm

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def homepage():
    events = Event.query.all()  
    return render_template('homepage.html', events=events)

@main_bp.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        title = request.form.get('eventName')
        description = request.form.get('eventDescription')
        date = request.form.get('eventDate')
        
        if not title or not description or not date:
            flash('All fields are required!', 'danger')
            return redirect(url_for('main.create_event'))
        
        new_event = Event(title=title, description=description, date=date, status='Open')
        db.session.add(new_event)
        db.session.commit()
        
        flash('Event created successfully!', 'success')
        return redirect(url_for('main.homepage'))
    
    return render_template('ECreation.html')

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
    event = Event.query.get(event_id)
    if event is None:
        return "Event not found", 404

    form = TicketBookingForm()  

    return render_template('EDetails.html', event=event, form=form)


@main_bp.route('/trigger-500')
def trigger_500():
    return 1 / 0
