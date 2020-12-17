From ubuntu:focal

# MongoDB installation
RUN wget -qO - https://www.mongodb.org/static/pgp/server-4.4.asc | apt-key add - \
    echo "deb [ arch=amd64,arm64 ] https://repo.mongodb.org/apt/ubuntu focal/mongodb-org/4.4 multiverse" | tee /etc/apt/sources.list.d/mongodb-org-4.4.list \
    apt-get update \
    apt-get install -y mongodb-org=4.4.2 mongodb-org-server=4.4.2 mongodb-org-shell=4.4.2 mongodb-org-mongos=4.4.2 mongodb-org-tools=4.4.2

# Elasticsearch installation
RUN wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add - \
    echo "deb https://artifacts.elastic.co/packages/oss-7.x/apt stable main" | sudo tee /etc/apt/sources.list.d/elastic-7.x.list \
    apt-get update \
    apt-get install elasticsearch-oss=7.10.1

# Initialize python venv
    

# Initialize elasticsearch
RUN curl -XPUT localhost:9200/package_info -H 'Content-Type: application/json' -d '{"mappings":{ "properties": {"author": {"type": "text"}, "author_email": {"type": "keyword"}, "description": {"type": "text"}, "keywords": {"type": "keyword"}, "version": {"type": "keyword"}, "maintainer": {"type": "text"}, "maintainer_email":{"type": "keyword"}, "name": {"type": "keyword"}}}}' 

# Initialize mongodb

