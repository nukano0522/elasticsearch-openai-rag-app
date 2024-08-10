# FROM docker.elastic.co/elasticsearch/elasticsearch:8.11.1
FROM docker.elastic.co/elasticsearch/elasticsearch:8.13.0
RUN ./bin/elasticsearch-plugin install analysis-kuromoji
RUN ./bin/elasticsearch-plugin install analysis-icu