from sqlalchemy.exc import IntegrityError

from flask import  request, jsonify, Response
from flask_expects_json import expects_json

from app.db import db
from app import app
from app.models import User, Telegram, TelegramGroupId
from app.token import token_required
from app.schema.telegram_schema import token_schema, group_schema


@app.route('/telegram/token', methods=['POST'])
@token_required
@expects_json(token_schema)
def post_telegram_token(current_user):
    request_data = request.get_json()

    telegram = Telegram(user_id=current_user.id, token=request_data.get('token'), name=request_data.get('name'))

    try:
        db.session.add(telegram)
        db.session.commit()
    except IntegrityError:
        return Response("{'message': 'telegram token already exists.'}", status=400)

    return jsonify({'token_id': telegram.id})


@app.route('/telegram/<token_id>/group', methods=['POST'])
@token_required
@expects_json(group_schema)
def post_telegram_group(current_user, token_id):
    request_data = request.get_json()

    token = Telegram.query.filter_by(user_id=current_user.id, id=token_id).first()

    if not token:
        return Response("{'message': 'telegram token does not exist.'}", status=404)

    new_group = TelegramGroupId(token_id=token_id, name=request_data.get('name'), group_id=request_data.get('group_id'))

    db.session.add(new_group)
    db.session.commit()

    return jsonify({'message': 'group has been added.'})


@app.route('/telegram/all', methods=['GET'])
@token_required
def get_all_tokens(current_user):
    tokens = Telegram.query.filter_by(user_id=current_user.id).all()

    data = []

    for token in tokens:
        token_data = {
            "id": token.id,
            "name": token.name,
            "token": token.token,
            "groups": []
        }

        groups = TelegramGroupId.query.filter_by(token_id=token.id).all()

        for group in groups:
            token_data["groups"].append({
                "id": group.id,
                "name": group.name,
                "group_id": group.group_id
            })

        data.append(token_data)

    return jsonify(data)


@app.route('/telegram/token/<token_id>/delete', methods=['DELETE'])
@token_required
def delete_token(current_user, token_id):
    token = Telegram.query.filter_by(user_id=current_user.id, id=token_id).first()

    if not token:
        return Response("{'message': 'telegram token does not exist.'}", status=404)

    db.session.delete(token)
    TelegramGroupId.query.filter_by(token_id=token.id).delete()
    db.session.commit()

    return jsonify({'message': 'telegram token has been deleted.'})
