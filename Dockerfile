FROM python:3.7

RUN apt-get update
RUN apt-get -y install git
RUN apt-get -y install sqlite3
RUN pip install gunicorn
RUN git clone https://github.com/Samba-Odoo-Apps/automl.git
#ADD . automl
RUN chmod -R 777 ./automl
RUN pip install -r ./automl/requirements.txt
ENTRYPOINT ["./automl/entry.sh"]
