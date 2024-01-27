# sbccl_webapp

Web application for Center for Chinese learning at Stony Brook. It's still under development.

# Prerequisite

## Libraries

In order to run this application, below are required libaries

- Django
- Djangorestframework
- django-cors-headers
- Apache
- python3
- Postgresql
- React. For frontend dependency, please see package.json under ./frontend folder. For instructions, please see ./frontend/README.md
- npm
- Bootstrap


# How to run the server

python3 manage.py runserver

# Migrate database if data model is changed

1. python3 manage.py makemigrates
2. python3 manage.py migrate
