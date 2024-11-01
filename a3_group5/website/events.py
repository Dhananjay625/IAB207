from flask import Blueprint, render_template, request, redirect, url_for
from .models import Event
from .import db

eventbp = Blueprint('event', __name__, url_prefix='/event')

@eventbp.route('/<int:id>')
def show(id):
    event = Event.query.get_or_404(id)
    return render_template('EDetails.html', event=event)

