FROM python:3.8

RUN mkdir /home/juliantorres/comprimemelo.com

WORKDIR /home/juliantorres/comprimemelo.com

COPY  . ./

RUN pip3 install --no-cache-dir -r requeriments.txt

EXPOSE 80

CMD ["flask", "nohup python -m flask --app main --debug run", "--host", "0.0.0.0","--port","80"]

