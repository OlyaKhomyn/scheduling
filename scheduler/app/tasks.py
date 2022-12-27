from celery import Celery
import requests

REDIS_URL = 'redis://redis:6379/0'
BROKER_URL = 'amqp://admin:mypass@rabbit//'

CELERY = Celery('tasks', backend=REDIS_URL, broker=BROKER_URL)


@CELERY.task()
def send_telegram(token, chat_id, text):
    requests.post(
        "http://messages:18888/bot-text",
        json={
            'token': token,
            'chat_id': chat_id,
            'text': text
        }
    )


@CELERY.task()
def send_email(username, password, title, recipients, body):
    requests.post(
        "http://messages:18888/email",
        json={
            'username': username,
            'password': password,
            'title': title,
            'recipients': recipients,
            'body': body
        }
    )


@CELERY.task()
def send_slack(token, channel, text):
    requests.post(
        "http://messages:18888/slack",
        json={
            'token': token,
            'channel': channel,
            'text': text
        }
    )
