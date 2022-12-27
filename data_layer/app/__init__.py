from flask import Flask

app = Flask(__name__)

from app.views.auth_views import *
from app.views.telegram_views import *
from app.views.email_views import *
from app.views.slack_views import *
