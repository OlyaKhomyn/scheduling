from sqlalchemy.exc import IntegrityError

from flask import  request, jsonify, Response
from flask_expects_json import expects_json

from app.db import db
from app import app

from app.models import User, Slack
from app.token import token_required
from app.schema.slack_schema import slack_schema


@app.route('/slack/token', methods=['POST'])
@token_required
@expects_json(slack_schema)
def post_slack_token(current_user):
    request_data = request.get_json()

    slack = Slack(user_id=current_user.id, bot_token=request_data.get('bot_token'),
                  user_token=request_data.get('user_token'), channel=request_data.get("channel_id"),
                  name=request_data.get('name'))

    try:
        db.session.add(slack)
        db.session.commit()
    except IntegrityError as e:
        return Response("{'message': 'slack token already exists.'}", status=400)

    return jsonify({'token_id': slack.id})


@app.route('/slack/all', methods=['GET'])
@token_required
def get_all_slack_tokens(current_user):
    slacks = Slack.query.filter_by(user_id=current_user.id).all()
    data = []

    for slack in slacks:
        data.append({
            "name": slack.name,
            "channel_id": slack.channel,
            "bot_token": slack.bot_token,
            "user_token": slack.user_token
        })

    return jsonify(data)


@app.route('/slack/token/<token_id>/delete', methods=['DELETE'])
@token_required
def delete_slack_token(current_user, token_id):
    token = Slack.query.filter_by(user_id=current_user.id, id=token_id).first()

    if not token:
        return Response("{'message': 'slack token does not exist.'}", status=404)

    db.session.delete(token)
    db.session.commit()

    return jsonify({'message': 'slack token has been deleted.'})
