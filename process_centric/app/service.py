import requests
from flask import request

from app.consts import *

def get_telegram_tokens():
    try:
        response = requests.get(f'{DATA_URL}/telegram/all', headers=request.headers)
    except Exception:
        return "unexpected errror", 500

    return response, response.status_code


def post_telegram(token, group, text, time):
    json = {
        'token': token,
        'chat_id': group,
        'text': text,
        "time": time if time else ""
    }
    try:
        response = requests.post(f'{SCHEDULER_URL}/schedule-bot', json=json, headers=request.headers)
    except Exception:
        return "unexpected error.", 500

    if response.status_code == 200:
        return "telegram message is set.", 200
    else:
        return response.text, response.status_code

def send_telegram_auth(text, bot_names, time=None):
    response, status = get_telegram_tokens()

    if status != 200:
        return response.text, status

    resp, status = "no such bot name", 400
    for tel_data in response.json():
        if tel_data['name'] in bot_names:
            for group in tel_data['groups']:
                resp , status = post_telegram(tel_data['token'], group['group_id'], text, time)

    return resp, status


def post_email(sender, password, title, recipients, body, time):
    json = {
        'username': sender,
        'password': password,
        'title': title,
        'recipients': recipients,
        'body': body,
        "time": time if time else ""
    }
    try:
        response = requests.post(f'{SCHEDULER_URL}/schedule-email', json=json, headers=request.headers)
    except Exception:
        return "unexpected errror", 500

    if response.status_code == 200:
        return "email message is set.", 200
    else:
        return response.text, response.status_code


def send_email_auth(body, title, sender, recipients, time):
    try:
        sender_response = requests.get(f'{DATA_URL}/email/sender/{sender}', headers=request.headers)
    except Exception:
        return "unexpected error.", 500

    if sender_response.status_code != 200:
        return sender_response.text, sender_response.status_code

    response, status = post_email(sender, sender_response.json()['password'], title, recipients, body, time)

    return response, status


def post_slack(channel, text, token, time):
    json = {
        'token': token,
        'channel': channel,
        'text': text,
        "time": time if time else ""
    }
    try:
        response = requests.post(f'{SCHEDULER_URL}/schedule-slack', json=json, headers=request.headers)
    except Exception:
        return "unexpected error.", 500

    if response.status_code == 200:
        return "slack message is set.", 200
    else:
        return response.text, response.status_code


def send_slack_auth(text, bots, time):
    try:
        data = requests.get(f'{DATA_URL}/slack/all', headers=request.headers)
    except Exception:
        return "unexpected error.", 500

    if data.status_code != 200:
        return data.text, data.status_code

    resp, status = "no such bot name", 400
    for data in data.json():
        for bot in bots:
            if bot["name"] == data["name"]:
                token = data["user_token"] if bot["type"] == "user" else data["bot_token"]
                resp, status = post_slack(data["channel_id"], text, token, time)

    return resp, status
