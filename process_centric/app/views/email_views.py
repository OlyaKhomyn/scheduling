import requests

from flask import request, Response

from app import app
from app.consts import *


@app.route('/email/sender', methods=['POST'])
def post_sender():
    response = requests.post(f'{DATA_URL}/email/sender', json=request.get_json(),
                             headers=request.headers)
    return Response(response.text, response.status_code)


@app.route('/email/recipients', methods=['POST'])
def post_recipients():
    response = requests.post(f'{DATA_URL}/email/recipients', json=request.get_json(),
                             headers=request.headers)
    return Response(response.text, response.status_code)


@app.route('/email/sender/<email>', methods=['GET'])
def get_sender(email):
    response = requests.get(f'{DATA_URL}/email/sender/{email}', headers=request.headers)

    return Response(response.text, response.status_code)


@app.route('/email/sender/all', methods=['GET'])
def get_senders():
    response = requests.get(f'{DATA_URL}/email/sender/all', headers=request.headers)

    return Response(response.text, response.status_code)


@app.route('/email/recipient/all', methods=['GET'])
def get_recipients():
    response = requests.get(f'{DATA_URL}/email/recipient/all', headers=request.headers)

    return Response(response.text, response.status_code)


@app.route('/email/sender/<email>/delete', methods=['DELETE'])
def delete_sender(email):
    response = requests.delete(f'{DATA_URL}/email/sender/{email}/delete', headers=request.headers)

    return Response(response.text, response.status_code)


@app.route('/email/recipient/<email>/delete', methods=['DELETE'])
def delete_recipient(email):
    response = requests.delete(f'{DATA_URL}/email/recipient/{email}/delete', headers=request.headers)

    return Response(response.text, response.status_code)
