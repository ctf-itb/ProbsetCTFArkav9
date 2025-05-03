FROM node:23-alpine3.20

WORKDIR /var/www/html

COPY . .
RUN npm i

EXPOSE 8020
CMD [ "node", "index.js" ]