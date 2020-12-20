#Package info from PyPi rss feed

This application enables a user to search for information regarding new and updated packages on PyPI python packages index.
It checks the PyPi rss feed daily for new updates, downloads information regarding the mentioned packages and uploads it to an internal database and full text search solution.

## General info

Most settings are controlled via environment settings with reasonable defaults.
Please check package_info/package_info/settings.py.

You'll most likely want to change:
- SECRET_KEY - set it to a random string with regular and capital letters + numbers and special chars
- ALLOWED_HOSTS - if you want to run in production, this needs to be a python list containing 


##Usage

The application is designed to run in a standalone docker container.
You can also run the app without docker if needed.

### Running in docker


### Running standalone
