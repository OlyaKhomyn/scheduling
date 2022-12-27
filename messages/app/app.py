import requests

from flask_expects_json import expects_json
from flask_mail import Mail, Message
from flask import Flask, request, Response

from .schema import email_schema, telegram_text_schema, slack_schema

app = Flask(__name__)

app.config['MAIL_SERVER'] = 'smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True


@app.route('/email', methods=['POST'])
@expects_json(email_schema)
def send_email():
    request_data = request.get_json()

    app.config['MAIL_USERNAME'] = request_data['username']
    app.config['MAIL_PASSWORD'] = request_data['password']

    mail = Mail(app)
    msg = Message(request_data['title'], sender=request_data['username'], recipients=request_data['recipients'])
    msg.body = request_data['body']

    try:
        mail.send(msg)
    except Exception:
        return Response("{'status':'error occurred while trying to send a message.'}", status=400,
                        mimetype='application/json')

    return Response("{'status':'message sent.'}", status=200, mimetype='application/json')


@app.route('/bot-text', methods=['POST'])
@expects_json(telegram_text_schema)
def send_from_bot():
    request_data = request.get_json()

    api_token = request_data['token']
    chat_id = request_data['chat_id']

    url = f'https://api.telegram.org/bot{api_token}/sendMessage'
    try:
        requests.post(url, json={'chat_id': chat_id, 'text': request_data['text']})
    except Exception:
        return Response("{'status':'error occurred while trying to send a message.'}", status=400,
                        mimetype='application/json')

    return Response("{'status':'message sent.'}", status=200, mimetype='application/json')


@app.route('/slack', methods=['POST'])
@expects_json(slack_schema)
def send_slack():
    request_data = request.get_json()

    text = request_data['text']
    channel = request_data['channel']
    token = request_data['token']

    url = 'https://slack.com/api/chat.postMessage'
    headers = {"Authorization": f"Bearer {token}"}

    try:
        requests.post(url, json={"channel": channel, "text": text}, headers=headers)
    except Exception:
        return Response("{'status':'error occurred while trying to send a message.'}", status=400,
                        mimetype='application/json')

    return Response("{'status':'message sent.'}", status=200, mimetype='application/json')
