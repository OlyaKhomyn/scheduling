import requests

from flask import request, Response

from app import app
from app.consts import *


@app.route('/telegram/token', methods=['POST'])
def post_token():
    response = requests.post(f'{DATA_URL}/telegram/token', json=request.get_json(),
                             headers=request.headers)
    return Response(response.text, response.status_code)


@app.route('/telegram/<token_id>/group', methods=['POST'])
def post_group(token_id):
    response = requests.post(f'{DATA_URL}/telegram/{token_id}/group', json=request.get_json(),
                             headers=request.headers)
    return Response(response.text, response.status_code)


@app.route('/telegram/all', methods=['GET'])
def get_tokens():
    response = requests.get(f'{DATA_URL}/telegram/all', headers=request.headers)
    return Response(response.text, response.status_code)


@app.route('/telegram/token/<token_id>/delete', methods=['DELETE'])
def delete_token(token_id):
    response = requests.delete(f'{DATA_URL}/telegram/token/{token_id}/delete', headers=request.headers)
    return Response(response.text, response.status_code)
