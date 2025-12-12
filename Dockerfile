FROM php:7.4-fpm-bullseye

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
    git unzip wget curl gnupg2 \
    libicu-dev g++ libpng-dev libjpeg-dev libfreetype6-dev \
    libxslt1-dev zlib1g-dev libzip-dev \
    imagemagick ghostscript poppler-utils openjdk-11-jre-headless \
    build-essential autoconf pkg-config re2c \
    default-mysql-client \
    && rm -rf /var/lib/apt/lists/*

# --- Extensiones PHP ---
RUN docker-php-ext-install intl
RUN docker-php-ext-install pdo pdo_mysql
RUN docker-php-ext-configure gd --with-freetype --with-jpeg \
    && docker-php-ext-install gd
RUN docker-php-ext-install xsl
RUN docker-php-ext-install zip
RUN docker-php-ext-install opcache

# APCu
RUN pecl install apcu \
    && docker-php-ext-enable apcu

# --- Composer ---
RUN curl -sS https://getcomposer.org/installer | php \
    -- --install-dir=/usr/local/bin --filename=composer

# Configuración de PHP
RUN echo "[PHP]" > /usr/local/etc/php/conf.d/atom.ini && \
    echo "memory_limit=1024M" >> /usr/local/etc/php/conf.d/atom.ini && \
    echo "error_reporting = E_ALL" >> /usr/local/etc/php/conf.d/atom.ini && \
    echo "display_errors = On" >> /usr/local/etc/php/conf.d/atom.ini && \
    echo "display_startup_errors = On" >> /usr/local/etc/php/conf.d/atom.ini && \
    echo "log_errors = On" >> /usr/local/etc/php/conf.d/atom.ini && \
    echo "error_log = /var/log/php_errors.log" >> /usr/local/etc/php/conf.d/atom.ini

# --- Descargar AtoM 2.8.2 (Tarball con assets compilados) ---
RUN wget -q https://storage.accesstomemory.org/releases/atom-2.8.2.tar.gz && \
    tar xzf atom-2.8.2.tar.gz -C /var/www/html --strip-components=1 && \
    rm atom-2.8.2.tar.gz

WORKDIR /var/www/html

# Ajuste de permisos inicial
RUN chown -R www-data:www-data /var/www/html

# Copiar vendor/symfony con Symfony 1.4 correcto
RUN if [ -d "/var/www/html/symfony1-1.4.20" ]; then \
    rm -rf /var/www/html/vendor/symfony 2>/dev/null; \
    cp -r /var/www/html/symfony1-1.4.20 /var/www/html/vendor/symfony; \
    fi

# Permisos
RUN chown -R www-data:www-data /var/www/html
RUN mkdir -p /var/www/html/cache /var/www/html/log /var/www/html/uploads
RUN chown -R www-data:www-data /var/www/html/cache /var/www/html/log /var/www/html/uploads
RUN chmod -R 775 /var/www/html/cache /var/www/html/log /var/www/html/uploads

# Log de errores PHP
RUN touch /var/log/php_errors.log && chmod 666 /var/log/php_errors.log

# Copiar script de entrada
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Puerto FPM
EXPOSE 9000

CMD ["/entrypoint.sh"]
