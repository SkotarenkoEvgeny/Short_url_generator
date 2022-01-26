## Short url service

In this service you can input long url and get short url.

Short url can be available 1-365 days (default)

This project use clearer SQLlite database


### installation

download repository

- installing dependencies. Open a console in the current folder and enter:
```sh
python3 -m venv myvenv
C:<path to directory> myvenv \ Scripts \ activate
pip install requirements.txt
```
or
```sh
pipenv install
```
after successful installation, to run the program, type in the console
```sh
python wsgi.py
```
For your comfort, you can use apidocs (http://localhost:5000/apidocs/).
Use methods: 
- DELETE/{short_url} Use http://localhost:5000/{short_url} or set short_url for 
  request.
  - GET/{short_url} Use http://localhost:5000/{short_url} or set short_url 
    for request.
- POST Set JSON ({"last_time": "integer", "original_url": "string"}). Not 
  use POST/{short_url}.
