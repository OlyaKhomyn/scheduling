from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import load_only

from flask import  request, jsonify, Response
from flask_expects_json import expects_json

from app.db import db
from app import app
from app.models import User, Email, EmailRecipients
from app.token import token_required
from app.schema.email_schema import sender_schema, recipients_schema


@app.route('/email/sender', methods=['POST'])
@token_required
@expects_json(sender_schema)
def post_sender(current_user):
    request_data = request.get_json()
    email = request_data.get('email')
    password = request_data.get('password')

    sender = Email(user_id=current_user.id, email=email, password=password)

    try:
        db.session.add(sender)
        db.session.commit()
    except IntegrityError:
        return Response(str({'message': f'email {email} already exists.'}), status=400)

    return jsonify({'email_id': sender.id})

@app.route('/email/recipients', methods=['POST'])
@token_required
@expects_json(recipients_schema)
def post_recipients(current_user):
    request_data = request.get_json()

    for email in request_data.get('emails'):
        recipient = EmailRecipients(user_id=current_user.id, email=email)
        db.session.add(recipient)
    db.session.commit()

    return jsonify({'message': 'recipients have been added.'})


@app.route('/email/sender/<email>', methods=['GET'])
@token_required
def get_sender(current_user, email):
    sender = Email.query.filter_by(user_id=current_user.id, email=email).first()

    if not sender:
        return Response(str({'message': f'email {email} does not exist.'}), status=404)

    return jsonify({'email': sender.email, 'password': sender.password})


@app.route('/email/sender/all', methods=['GET'])
@token_required
def get_senders(current_user):
    senders = Email.query.filter_by(user_id=current_user.id).options(load_only("email")).all()
    senders = [sender.email for sender in senders]

    return jsonify({'sender emails': senders})


@app.route('/email/recipient/all', methods=['GET'])
@token_required
def get_recipients(current_user):
    recipients = EmailRecipients.query.filter_by(user_id=current_user.id).options(load_only("email")).all()
    recipients = [recipient.email for recipient in recipients]

    return jsonify({'recipient emails': recipients})


@app.route('/email/sender/<email>/delete', methods=['DELETE'])
@token_required
def delete_sender(current_user, email):
    sender = Email.query.filter_by(user_id=current_user.id, email=email).first()

    if not sender:
        return Response(str({'message': f'email {email} does not exist.'}), status=400)

    db.session.delete(sender)
    db.session.commit()

    return jsonify({'message': 'email has been deleted.'})


@app.route('/email/recipient/<email>/delete', methods=['DELETE'])
@token_required
def delete_recipient(current_user, email):
    recipient = EmailRecipients.query.filter_by(user_id=current_user.id, email=email).first()

    if not recipient:
        return Response(str({'message': f'email {email} does not exist.'}), status=400)

    db.session.delete(recipient)
    db.session.commit()

    return jsonify({'message': 'email has been deleted.'})
