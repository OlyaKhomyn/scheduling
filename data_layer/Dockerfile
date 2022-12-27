FROM python:3.9-alpine

ADD data_layer/requirements.txt /app/requirements.txt

ENV PYTHONPATH "${PYTHONPATH}:/data_layer/app"

WORKDIR /app/

RUN pip install -r requirements.txt

EXPOSE 18888

ENTRYPOINT ["python3"]

CMD ["data_layer/app.py"]
