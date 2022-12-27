import requests

from flask import request, Response

from app import app
from app.consts import *


@app.route('/register', methods=['POST'])
def register():
    response = requests.post(f'{DATA_URL}/register', json=request.get_json(),
                             headers=request.headers)
    return Response(response.text, response.status_code)


@app.route('/login', methods=['POST'])
def login():
    response =  requests.post(f'{DATA_URL}/login', headers=request.headers)
    return Response(response.text, response.status_code)
