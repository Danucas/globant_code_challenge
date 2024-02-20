# globant_code_challenge


## REST API

Application Setup

this app was built with the help of [desktop-wrapper](https://pypi.org/project/desktop-wrapper/)

## Build the image

```
$ docker build -t globant-code-challenge .
```

## Run the container

```
$ docker run -p 4000:4000 --name code-challenge-api globant-code-challenge
```


## Run unittest

```
$ pytest
```

## Run integration tests

```
$ python -m app.integration_tests.db_test
```