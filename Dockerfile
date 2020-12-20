From ubuntu:focal-20201106

# Add project things
RUN apt-get update && \
    apt-get install -y python3-venv python3-dev build-essential sudo && \
    apt-get clean

# MariaDB installation
RUN apt-get update && \
    apt-get install -y mariadb-server=1:10.3.25-0ubuntu0.20.04.1 mariadb-client=1:10.3.25-0ubuntu0.20.04.1 libmariadbclient-dev=1:10.3.25-0ubuntu0.20.04.1 && \
    mkdir -p /data/mysql/data && \
    mkdir -p /data/mysql/logs && \
    apt-get clean
COPY confs_for_docker/99-mariadb.cnf /etc/mysql/mariadb.conf.d/99-mariadb.cnf

# Elasticsearch installation
RUN apt-get update && \
    apt-get install -y curl gnupg && \
    curl https://artifacts.elastic.co/GPG-KEY-elasticsearch | apt-key add - && \
    echo "deb https://artifacts.elastic.co/packages/oss-7.x/apt stable main" | tee /etc/apt/sources.list.d/elastic-7.x.list && \
    apt-get update && \
    apt-get install -y elasticsearch-oss=7.10.1 && \
    apt-get clean && \
    mkdir -p /data/elasticsearch/data && \
    mkdir -p /data/elasticsearch/logs

COPY confs_for_docker/elasticsearch.yml /etc/elasticsearch/elasticsearch.yml

COPY package_info /app

RUN python3 -m venv /app/venv && \
    /app/venv/bin/pip3 install -r /app/package_info/requirements.txt

ENTRYPOINT ["/bin/bash"]
CMD ["/app/run_docker.sh"]
WORKDIR "/app"
EXPOSE 8000
