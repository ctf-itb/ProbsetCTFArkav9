#!/bin/bash
set -e

if [ "$1" = 'php-fpm' ]; then
    mkdir -p /var/www/public/uploads
    chmod 1770 /var/www/public/uploads
    chown -R root:www-data /var/www/public/uploads
    touch /var/www/public/uploads/index.php
    chmod 000 /var/www/public/uploads/index.php
fi

exec "$@"