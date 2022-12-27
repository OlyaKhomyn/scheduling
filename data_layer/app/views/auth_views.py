import jwt
import uuid
import datetime

from flask import request, jsonify, make_response
from werkzeug.security import generate_password_hash, check_password_hash

from app.db import db
from app import app
from app.models import User


@app.route('/register', methods=['POST'])
def signup_user():
    data = request.get_json()

    hashed_password = generate_password_hash(data['password'], method='sha256')

    new_user = User(public_id=str(uuid.uuid4()), username=data['username'], password=hashed_password)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({'message': 'registeration successfully'})


@app.route('/login', methods=['POST'])
def login_user():
    auth = request.authorization

    if not auth or not auth.username or not auth.password:
        return make_response('could not verify', 401, {'Authentication': 'login required"'})

    user = User.query.filter_by(username=auth.username).first()

    if not user:
        return make_response('wrong username', 401, {'Authentication': 'login required"'})

    if check_password_hash(user.password, auth.password):
        token = jwt.encode(
            {'public_id': user.public_id, 'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=45)},
            app.config['SECRET_KEY'], "HS256")
        return jsonify({'token': token})

    return make_response('could not verify', 401, {'Authentication': '"login required"'})
