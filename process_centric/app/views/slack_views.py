import requests

from flask import request, Response

from app import app
from app.consts import *


@app.route('/slack/token', methods=['POST'])
def post_slack_token():
    response = requests.post(f'{DATA_URL}/slack/token', json=request.get_json(), headers=request.headers)
    return Response(response.text, response.status_code)


@app.route('/slack/all', methods=['GET'])
def get_slack_tokens():
    response = requests.get(f'{DATA_URL}/slack/all', headers=request.headers)
    return Response(response.text, response.status_code)


@app.route('/slack/token/<token_id>/delete', methods=['DELETE'])
def delete_slack_token(token_id):
    response = requests.delete(f'{DATA_URL}/slack/token/{token_id}/delete', headers=request.headers)
    return Response(response.text, response.status_code)
