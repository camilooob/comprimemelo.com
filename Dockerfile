FROM python:3.10-slim

ENV PYTHONUNBUFFERED True

ENV APP_HOME /app

WORKDIR $APP_HOME

COPY . ./

RUN pip3 install mysql-connector-python

RUN pip3 install pymysql

RUN pip3 install MySQL-python

RUN pip3 install --no-cache-dir -r requirements.txt

RUN pip3 install Flask gunicorn

RUN pip3 install --upgrade flask_login

ENV PORT=8080

EXPOSE 8080
# Run the web service on container startup. Here we use the gunicorn
CMD exec gunicorn --bind :$PORT --workers 1 --threads 8 --timeout 0 main:app