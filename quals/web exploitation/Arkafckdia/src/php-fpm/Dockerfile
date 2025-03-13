FROM php:7.2-fpm

RUN docker-php-ext-install pdo pdo_mysql

COPY docker-entrypoint.sh /docker-entrypoint.sh
RUN chmod +x /docker-entrypoint.sh

ENTRYPOINT ["bash", "/docker-entrypoint.sh"]

RUN usermod -u 33 www-data
RUN groupmod -g 33 www-data

CMD ["php-fpm"]

EXPOSE 9000
