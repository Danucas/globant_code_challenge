# globant_code_challenge

Live [CODE CHALLENGE API](https://globantchallenge.sytes.net/apidocs/)

## REST API for HR Calculations

### Requirements

- Python 3.8 or higher
- Docker

### Application Stack

- Flask (Backend)
- SQLAlchemy (DB Engine)
- SQLite (DB) can be extended to other SQL DBs


### Application Setup

This app was built on top of [desktop-wrapper](https://pypi.org/project/desktop-wrapper/)


### Build Project

Create the image with a custom tag

```
$ docker build -t globant-code-challenge .
```

### Run Docker

Create and run the container using the new custom Image, and route the 4000 default port from the container to the host

```
$ docker run -p 4000:4000 --name code-challenge-api globant-code-challenge
```

### Check the API specs

Go to [Swagger API Specs](http://localhost:4000/apidocs)


### Run unittest

At the root of the repo run

```
$ pytest
```

### Run integration tests

```
$ python -m app.integration_tests.db_test
```