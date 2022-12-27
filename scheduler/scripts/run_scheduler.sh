#!/bin/sh
cd scheduler/app
su -m app
python -m flask run --host=0.0.0.0 --port=18888