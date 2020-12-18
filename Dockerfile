From ubuntu:focal

# MongoDB installation
RUN apt-key adv --fetch-keys 'https://mariadb.org/mariadb_release_signing_key.asc' \
    echo "deb [arch=amd64] http://mariadb.mirror.globo.tech/repo/10.5/ubuntu focal main" | tee /etc/apt/sources.list.d/mariadb.list \
    apt-get update \
    apt-get install -y mariadb-server mariadb-client

# Elasticsearch installation
RUN wget -qO - https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add - \
    echo "deb https://artifacts.elastic.co/packages/oss-7.x/apt stable main" | tee /etc/apt/sources.list.d/elastic-7.x.list \
    apt-get update \
    apt-get install elasticsearch-oss=7.10.1

# Initialize python venv

# Initialize elasticsearch

# Initialize mongodb
