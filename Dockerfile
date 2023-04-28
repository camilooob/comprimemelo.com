FROM python:3.8

WORKDIR /opt/app

COPY requirements.txt .

# Install app dependencies

RUN pip3 install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 5000

ENTRYPOINT nohup python -m flask --app main --debug run --host=0.0.0.0 --port 8000 &

