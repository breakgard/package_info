#Package info from PyPi rss feed

This application enables a user to search for information regarding new and updated packages on PyPI python packages index.
It checks the PyPi rss feed daily for new updates, downloads information regarding the mentioned packages and uploads it to an internal database and elasticsearch.

A user is able to query the elasticsearch cluster via a single input field.

## General info

Most settings are controlled via environment variables with reasonable defaults.
Please check package_info/package_info/settings.py.

## Usage

### Required settings/prerequisites

This app is designed to work with MariaDB/MySQL and Elasticsearch.
You will need to have a working instances of those (unless you run the app using included Dockerfile, which creates an image that has those contained).

You'll most likely want to change:
- DJANGO_SECRET_KEY - set it to a random string with regular and capital letters + numbers and special chars. Example: `e97r8b!cf!#4=l==n@!%5j@lynys!!#=v4u=!zq=p1&3%p&^29`
- DJANGO_ALLOWED_HOSTS - if you want to run in production, this needs to be a python list containing IPs and domain names how the app is going to be accessed: Example: `['127.0.0.1', 'localhost']`

Unless running in docker, you'll most likely need to change:
- DJANGO_DEBUG - You'll probably want to set this to `True` when running with `python3 manage.py runserver`.
- DJANGO_DB_* - variables for connecting to the MariaDB host. Check settings.py.
- SEARCH_ELASTICSEARCH_HOSTS - Set this to a comma-delimited string containing Elasticsearch instances that the app will use. Example: `host1:9200,host2:9200`

If running using docker in production you'll probably want to launch with a volume for the /data folder, so data persists after container recreation.

There are other variables that control the app, like the following:
- SEARCH_PAGINATION_SIZE - controls how many package info entries matching the query are displayed on a single page of results. Default: `20`

### Running in docker

To build the docker container (while in project directory):
```
  docker build . --tag <optionally_your_repo_url>package_info:<some_tag>
  docker push <optionally_your_repo_url>package_info:<some_tag>
```
To start the docker container:
```
  docker run -v package_info_data:/data -e <required_environment_var1>=<value> -e <required_environment_var2>=<value> -p 8000:8000 <optionally_your_repo_url>package_info:<some_tag>
```
For debug/test mode:
```
  docker run -e DJANGO_DEBUG=True -p 8000:8000 github_test:0.0.1
```
To interact with django container (for example flush database), get inside the docker container using the following:
```
    docker exec -it <running_search_container_id> /bin/bash
    . venv/bin/activate
    python3 manage.py flush
    python3 manage.py search_index --rebuild
```

## Post install steps

To launch the periodic gathering of packages, launch the following url after running the server:

`http(s)://<search_app_url>/schedule_package_load`

## Exposed urls

- `/` - index page contains the search form
- `/result` - contains result of query (needs parameter `query`)
- `/get_max` - matches all documents, returns as many docs as `SEARCH_MAX_DOCUMENTS_RETURNED` environment variable allows
- `/load_packages` - launches a load packages from rss feed
- `/schedule_package_load` - schedules a background task for perodic loading of packages
- `/api/search_package_info` - same as `/result`, but returns json response

## To-Do

- Get an improved .css layout
- Add actual webserver config in docker (nginx - most probably wsgi reverse proxy)
- Create a docker-compose and get elasticsearch, nginx and mysql into separate containers
- Expand readme - add info on running outside of docker
