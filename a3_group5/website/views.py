from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Event, Booking, db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def homepage():
    events = Event.query.all()  
    return render_template('homepage.html', events=events)

@main_bp.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    if request.method == 'POST':
        title = request.form.get('eventName')
        description = request.form.get('eventDescription')
        date = request.form.get('eventDate')

        if not title or not description or not date:
            flash('All fields are required!', 'danger')
            return redirect(url_for('main.create_event'))

        # Create new event
        new_event = Event(title=title, description=description, date=date, status='Open')
        db.session.add(new_event)
        db.session.commit()

        flash('Event created successfully!', 'success')
        return redirect(url_for('main.homepage'))
    
    return render_template('ECreation.html')

@main_bp.route('/booking', methods=['GET', 'POST'])
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
            
            # Create new booking
            new_booking = Booking(quantity=quantity, price=price, user_id=current_user.id, event_id=event_id)
            db.session.add(new_booking)
            db.session.commit()

            flash('Booking confirmed!', 'success')
            return redirect(url_for('main.homepage'))
        
        except ValueError:
            flash('Invalid input. Please enter a valid number for tickets.', 'danger')
            return redirect(url_for('main.booking'))

    return render_template('booking.html', events=events)
print("main_bp is defined in views.py")