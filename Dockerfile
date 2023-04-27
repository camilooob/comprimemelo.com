FROM python:3.8

# Install app dependencies
COPY requirements.txt ./

RUN pip3 install --no-cache-dir -r requirements.txt

RUN mkdir -p app

EXPOSE 5000

CMD ["flask", "nohup python -m flask --app main --debug run", "--host", "0.0.0.0","--port","80"]

