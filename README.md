# aiPoll-server
aiPoll Server is a Django-based web application that provides an API for creating and managing polls. It also supports user registration and authentication.

## Features
 - User registration and authentication
 - Create, retrieve, update, and delete operations for polls
 - Commenting on polls
 - Chatbox for each poll
## Installation
 - Clone the repository
 - Install the dependencies using Pipenv: pipenv install
 - Set the environment variables for the database URL
 - Run the server: `python manage.py runserver`
## API Endpoints
 - `/register/`: Register a new user
 - `/login/`: Log in a user
 - `/polls/`: Create, retrieve, update, and delete polls
 - `/comments/`: Create, retrieve, update, and delete comments
 - `/chatboxes/`: Retrieve comments from a chatbox
## Dependencies
 - Django 4.2.3
 - Django Rest Framework 3.14.0
 - asgiref 3.7.2
 - pytz 2023.3
 - sqlparse 0.4.4
## License
MIT