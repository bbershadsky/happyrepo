# HappyRepo

[![Build Status](https://travis-ci.org/bbershadsky/happyrepo.svg?branch=master)](https://travis-ci.org/bbershadsky/happyrepo)
[![Built with](https://img.shields.io/badge/Built_with-Cookiecutter_Django_Rest-F7B633.svg)](https://github.com/agconti/cookiecutter-django-rest)

Django RESTFul API for daily check-ins and monitoring of happiness of multiple teams. Check out the project's [documentation](http://bbershadsky.github.io/happyrepo/).

## Features

* Django 3.2.5
* Django Rest Framework 3.12.4
* PostgreSQL 11.6
* PGAdmin web on port 5050
* Docker/Docker-compose + gunicorn

## Prerequisites

* [Docker](https://docs.docker.com/docker-for-mac/install/)  

## Local Deployment

Start the dev server for local deployment:

```bash
docker-compose up
```

## Create a superuser for Django Admin

```bash
docker-compose run --rm web python manage.py createsuperuser
<admin@admin.com>
<hunter2>
```

## Performing migrations

```bash
docker-compose run --rm web python manage.py makemigrations; docker-compose run --rm web python manage.py migrate
```

## Logging into Django Admin to add Users

[Django Administration](http://localhost:8000/admin/users/user/)

Use the credentials from above or your own.

## Creating new team member through cURL

```bash
curl -d '{"username":"'"$RANDOM"'", "password":"hunter2", "email":"happy@django.com", "first_name":"Django", "last_name":"General"}' \
     -H "Content-Type: application/json" \
     -X POST http://localhost:8000/api/v1/users/
```

Result:

```json
{
    "id":"5b311444-5ff6-41f7-81ea-33d99692f4eb","username":"8225","first_name":"Django","last_name":"General","email":"happy@django.com","auth_token":"546d2e559fe103f2a2f7eff29bf6309ab2a7623c"
}
```

## Logging in with credentials to obtain a token

Authorization tokens are issued and returned when a user registers. A registered user can also retrieve their token with the following request:

**Request**:

`POST` `api-token-auth/`

Parameters:

Name | Type | Description
---|---|---
username | string | The user's username
password | string | The user's password

**Response**:

```json
{ 
    "token" : "9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b" 
}
```

For clients to authenticate, the token key should be included in the Authorization HTTP header. The key should be prefixed by the string literal "Token", with whitespace separating the two strings. For example:

```text
Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b
```

The curl command line tool may be useful for testing token authenticated APIs. For example:

```bash
curl -X GET http://localhost:8000/api/v1/example/ -H 'Authorization: Token 9944b09199c62bcf9418ad846dd0e4bbdfc6ee4b'
```

## Submitting a rating (You can also use the DRF Browsable API)

POST http://localhost:8000/api/v1/rating/

```json
{
    "rating_score": 5,
    "user": "http://localhost:8000/api/v1/users/1/",
    "date": "2021-08-05"
}
```

NOTE: You may only submit one rating per day.

## View Statistics of User's team

Make sure you add the "Authorization: Token XXX" to your request headers

GET http://localhost:8000/api/v1/stats/

```json
{
  "user": "admin",
  "user's_team": "Backend",
  "*": 0,
  "**": 0,
  "***": 1,
  "****": 1,
  "*****": 2,
  "team_averages": 4.25
}
```

## View Statistics of all teams (not logged in)

GET http://localhost:8000/api/v1/stats/

Result:

```json
{
    "Team Average Happiness": 3.38
}
```

## Accessing the Django Shell within Docker container

```bash
docker-compose run --rm web python manage.py shell
from happyrepo.users.models import User, Rating
```
