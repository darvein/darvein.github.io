FROM python:3.9.18-slim

WORKDIR /usr/src/app

RUN pip install requests

COPY app.py .

CMD [ "python", "./app.py" ]
