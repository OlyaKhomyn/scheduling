#!/bin/sh
cd scheduler/app
su -m app -c "celery -A tasks worker --loglevel INFO"