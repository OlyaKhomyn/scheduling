from flask import Flask

from app.converter import StringListConverter

app = Flask(__name__)
app.url_map.converters['str_list'] = StringListConverter


from app.views.telegram_views import *
from app.views.email_views import *
from app.views.auth_views import *
from app.views.tasks_views import *
from app.views.slack_views import *