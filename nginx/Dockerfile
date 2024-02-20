FROM nginx
COPY ./certs/fullchain.pem /ssl/fullchain.pem
COPY ./certs/privkey.pem /ssl/privkey.pem
COPY ./nginx.conf /etc/nginx/nginx.conf

RUN ls -lah /ssl