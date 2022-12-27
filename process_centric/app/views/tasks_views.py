from flask import request, Response

from app import app
from app.task_handler import TaskHandler, NoAuthTaskHandler


@app.route('/set-message/<str_list:services>', methods=['POST'])
def set_message(services):
    task_handler = TaskHandler(services, request.get_json())

    response, status = task_handler.parse_services()

    return Response(response, status)

@app.route('/set-message-no-auth/<str_list:services>', methods=['POST'])
def set_message_no_auth(services):
    task_handler = NoAuthTaskHandler(services, request.get_json())

    response, status = task_handler.parse_services()


    return Response(response, status)
