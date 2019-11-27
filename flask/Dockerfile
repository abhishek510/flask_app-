FROM python:3.7.2-stretch

WORKDIR /

ADD . /

RUN chmod 777 app.log

RUN pip install -r requirements.txt

CMD ["uwsgi","app.ini"]
