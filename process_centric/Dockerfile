FROM python:latest

ADD process_centric/requirements.txt /app/requirements.txt

WORKDIR /app/

RUN pip install -r requirements.txt

ENTRYPOINT ["python3"]

CMD ["process_centric/app.py"]
