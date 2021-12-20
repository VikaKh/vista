FROM python:3.8-buster

# install nginx
RUN apt-get update && apt-get install nginx vim -y --no-install-recommends && apt-get install gettext-base

ARG DB_NAME
ARG DB_USER
ARG DB_PASSWORD
ARG DB_HOST
ARG DB_PORT

ENV DB_NAME vistamed
ENV DB_USER developer
ENV DB_PASSWORD development
ENV DB_HOST database-1.cuks1ppm363o.eu-central-1.rds.amazonaws.com
ENV DB_PORT 3306
# copy source and install dependencies
RUN mkdir -p /opt/app

RUN mkdir -p /opt/app/smart_clinic
COPY ./nginx/start-server.sh /opt/app/
COPY core/ /opt/app/smart_clinic/core/
COPY nginx/ /opt/app/smart_clinic/nginx/
COPY smart_clinic/ /opt/app/smart_clinic/smart_clinic/
COPY vista_med/ /opt/app/smart_clinic/vista_med/
RUN envsubst < /opt/app/smart_clinic/smart_clinic/local_settings_template.py > /opt/app/smart_clinic/smart_clinic/local_settings.py
COPY manage.py /opt/app/smart_clinic/
COPY requirements.txt /opt/app/smart_clinic/
WORKDIR /opt/app/smart_clinic
RUN pip3 install -r requirements.txt
RUN python manage.py collectstatic
RUN python manage.py migrate

# start server
STOPSIGNAL SIGTERM
ENTRYPOINT ["sh", "/opt/app/start-server.sh"]