FROM nginx:1.27

# certbot stuff
RUN apt-get update && apt-get install -y --no-install-recommends certbot
RUN mkdir -p /etc/.well-known

RUN rm /etc/nginx/conf.d/default.conf
COPY nginx.conf /etc/nginx/conf.d
RUN echo "explorer:\$apr1\$Y85eAGBM\$cLh1KH0/Hd8B7j4GqzXir0" > /etc/nginx/.htpasswd
