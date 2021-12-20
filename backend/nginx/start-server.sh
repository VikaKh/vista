#!/usr/bin/env bash
# start-server.sh
(envsubst < /opt/app/smart_clinic/nginx/nginx.default.template > /etc/nginx/sites-available/default) &
(gunicorn smart_clinic.wsgi --bind 0.0.0.0:8000) &
nginx -g "daemon off;"