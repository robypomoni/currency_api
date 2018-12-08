Currency API
==============

API to convert currencies based on Django REST Framework

Installation
==============
Make sure to have `Docker <https://docs.docker.com/install/>`_ and `Docker Compose <https://docs.docker.com/compose/install/>`_ installed on your sistem.

- Clone the repository
- Cd to the repository directory
- Run "docker-compose up" for production environment, or "docker-compose -f docker-compose-dev.yml up" for development environment
- wait until containers ar up and database is populated (it takes a while)
- API is ready at http://localhost/api/currency/