FROM nginx:1.27

# certbot stuff
RUN apt-get update -y; apt-get install -y --no-install-recommends certbot
RUN mkdir -p /etc/.well-known

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
