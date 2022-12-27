import jwt

from flask import request, jsonify, Response
from functools import wraps

from app import app
from app.models import User


def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None

        if 'x-access-tokens' in request.headers:
             token = request.headers['x-access-tokens']

        if not token:
            return Response("{'message': 'a valid token is missing'}", status=401)

        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = User.query.filter_by(public_id=data['public_id']).first()
        except:
            return Response("{'message': 'token is invalid'}", status=401)

        return f(current_user, *args, **kwargs)

    return decorator
