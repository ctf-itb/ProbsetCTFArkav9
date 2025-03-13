FROM nginx:latest

COPY nginx.conf /etc/nginx/

RUN usermod -u 33 www-data
RUN groupmod -g 33 www-data

CMD ["nginx"]
EXPOSE 80