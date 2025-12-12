FROM openjdk:8-jre-bullseye

# Crear usuario elasticsearch
RUN groupadd -g 1000 elasticsearch && \
    useradd -u 1000 -g 1000 -d /usr/share/elasticsearch elasticsearch

# Instalar dependencias necesarias
RUN apt-get update && apt-get install -y wget curl && rm -rf /var/lib/apt/lists/*

# Descargar e instalar Elasticsearch 5.6.16
WORKDIR /usr/share/elasticsearch
RUN wget https://artifacts.elastic.co/downloads/elasticsearch/elasticsearch-5.6.16.tar.gz && \
    tar -xzf elasticsearch-5.6.16.tar.gz --strip-components=1 && \
    rm elasticsearch-5.6.16.tar.gz

# Configuración básica
RUN mkdir -p /usr/share/elasticsearch/data /usr/share/elasticsearch/logs /usr/share/elasticsearch/config
COPY config/elasticsearch.yml /usr/share/elasticsearch/config/elasticsearch.yml

# Permisos
RUN chown -R elasticsearch:elasticsearch /usr/share/elasticsearch

# Cambiar a usuario elasticsearch
USER elasticsearch

# Variables de entorno por defecto
ENV ES_JAVA_OPTS="-Xms512m -Xmx512m"

EXPOSE 9200 9300

CMD ["bin/elasticsearch"]
