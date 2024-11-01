from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Event, Booking, db
from .forms import TicketBookingForm

# Create a Blueprint instance for your main routes
main_bp = Blueprint('main', __name__)

# Route for the homepage displaying all events
@main_bp.route('/')
def homepage():
    events = Event.query.all()  # Fetch all events from the database
    return render_template('homepage.html', events=events)

# Route for creating a new event
@main_bp.route('/create_event', methods=['GET', 'POST'])
def create_event():
    if request.method == 'POST':
        title = request.form.get('eventName')
        description = request.form.get('eventDescription')
        date = request.form.get('eventDate')
        
        if not title or not description or not date:
            flash('All fields are required!', 'danger')
            return redirect(url_for('main.create_event'))
        
        # Create a new event and add it to the database
        new_event = Event(title=title, description=description, date=date, status='Open')
        db.session.add(new_event)
        db.session.commit()
        
        flash('Event created successfully!', 'success')
        return redirect(url_for('main.homepage'))
    
    return render_template('ECreation.html')

# Route for booking an event
@main_bp.route('/booking', methods=['GET', 'POST'])
@login_required  # Ensure only logged-in users can access this route
def booking():
    events = Event.query.filter_by(status='Open').all()  # Fetch only events with status 'Open'
    
    if request.method == 'POST':
        event_id = request.form.get('selectEvent')
        quantity = request.form.get('ticketQuantity')
        
        if not event_id or not quantity:
            flash('Please select an event and specify the number of tickets.', 'danger')
            return redirect(url_for('main.booking'))
        
        try:
            quantity = int(quantity)  # Convert quantity to an integer
            price = 100 * quantity  # Calculate the price of tickets
            
            # Create a new booking and add it to the database
            new_booking = Booking(quantity=quantity, price=price, user_id=current_user.id, event_id=event_id)
            db.session.add(new_booking)
            db.session.commit()
            
            flash('Booking confirmed!', 'success')
            return redirect(url_for('main.homepage'))
        
        except ValueError:
            flash('Invalid input. Please enter a valid number for tickets.', 'danger')
            return redirect(url_for('main.booking'))
    
    return render_template('booking.html', events=events)

# Route for displaying event details
@main_bp.route('/event/<int:event_id>')
def event_details(event_id):
    # Query the event from the database using the provided event_id
    event = Event.query.get(event_id)
    if event is None:
        return "Event not found", 404

    # If you have a form object, import and initialize it
    form = TicketBookingForm()  # Replace 'YourFormClass' with your actual form class name

    # Render the event details template with the event and form data
    return render_template('EDetails.html', event=event, form=form)