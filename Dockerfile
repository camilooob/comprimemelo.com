FROM python:3.10-slim

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY . ./

RUN pip install mysql-connector-python

RUN pip install pymysql

RUN pip3 install --no-cache-dir -r requirements.txt

EXPOSE 8080
# Run the web service on container startup. Here we use the gunicorn
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app