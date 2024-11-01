from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from .models import Event, Comment
from .models import User
from . import db
import random

eventbp = Blueprint('event', __name__, url_prefix='/event')

@eventbp.route('/<int:id>')
def show(id):
    event = Event.query.get_or_404(id)
    return render_template('EDetails.html', event=event)



@eventbp.route('/<int:event_id>/comment', methods=['POST'])
@login_required
def add_comment(event_id):
    content = request.form.get('content')

    while True:
        comment_id = random.randint(100, 999)
        existing_comment = db.session.scalar(db.select(Comment).where(Comment.id == comment_id))
        if existing_comment is None:
            break

    if content:
        comment = Comment(id=comment_id, content=content, user_id=current_user.id, event_id=event_id)
        db.session.add(comment)
        db.session.commit()
    else:
        flash('Comment cannot be empty.')
    return redirect(url_for('event.show', id=event_id))

