import iso8601
import datetime

import tasks
import schema

from flask import Flask, request, Response
from flask_expects_json import expects_json


app = Flask(__name__)


def convert_to_utc(time):
    time = iso8601.parse_date(time).replace(tzinfo=datetime.timezone.utc)
    time = time - datetime.timedelta(hours=1)
    return time


@app.route('/schedule-email', methods=['POST'])
@expects_json(schema.email_schema, check_formats=True)
def schedule_email():
    request_data = request.get_json()

    args = [request_data['username'], request_data['password'],
            request_data['title'], request_data['recipients'], request_data['body']]

    if not request_data.get('time'):
        job = tasks.send_email.apply_async(args=args)
    else:
        time = convert_to_utc(request_data['time'])
        job = tasks.send_email.apply_async(args=args, eta=time, time_limit=10000000000, soft_time_limit=10000000000)

    return Response(f"task: {job.task_id}", status=200, mimetype='application/json')


@app.route('/schedule-bot', methods=['POST'])
@expects_json(schema.telegram_text_schema, check_formats=True)
def schedule_bot():
    request_data = request.get_json()

    args = [request_data['token'], request_data['chat_id'], request_data['text']]

    if not request_data.get('time'):
        job = tasks.send_telegram.apply_async(args=args)
    else:
        time = convert_to_utc(request_data['time'])
        job = tasks.send_telegram.apply_async(args=args, eta=time, time_limit=10000000000, soft_time_limit=10000000000)

    return Response(f"task: {job.task_id}", status=200, mimetype='application/json')


@app.route('/schedule-slack', methods=['POST'])
@expects_json(schema.slack_schema, check_formats=True)
def schedule_slack():
    request_data = request.get_json()

    args = [request_data['token'], request_data['channel'], request_data['text']]

    if not request_data.get('time'):
        job = tasks.send_slack.apply_async(args=args)
    else:
        time = convert_to_utc(request_data['time'])
        job = tasks.send_slack.apply_async(args=args, eta=time, time_limit=10000000000, soft_time_limit=10000000000)

    return Response(f"task: {job.task_id}", status=200, mimetype='application/json')
