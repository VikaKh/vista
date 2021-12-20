FROM nginx:alpine as production
COPY /nginx/nginx.conf.template /etc/nginx/nginx.conf.template

## Remove default nginx index page
RUN rm -rf /usr/share/nginx/html/*

# Copy from the stahg 1
COPY /build /usr/share/nginx/html

CMD /bin/sh -c "envsubst '\$PORT' < /etc/nginx/nginx.conf.template > /etc/nginx/nginx.conf" && nginx -g 'daemon off;'
