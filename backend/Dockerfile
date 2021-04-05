FROM python:3.9-slim-buster

COPY requirements.txt /tmp/

RUN pip install -r /tmp/requirements.txt

RUN useradd --create-home appuser
WORKDIR /home/appuser
USER appuser

COPY . .

RUN export FLASK_APP=main.py
CMD [ "python", "-m", "flask", "run"]