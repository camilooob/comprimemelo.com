FROM python:3.8

COPY  . ./

RUN pip3 install --no-cache-dir -r requeriments.txt

EXPOSE 80

CMD ["flask", "nohup python -m flask --app main --debug run", "--host", "0.0.0.0","--port","80"]

