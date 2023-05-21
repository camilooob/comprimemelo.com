FROM python:3.10-slim

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY . ./

RUN pip install mysql-connector-python

RUN pip install pymysql

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8080

ENV HOST=0.0.0.0
ENV PORT=8080

ENTRYPOINT nohup python -m flask --app main --debug run --host=0.0.0.0 --port 8080 &