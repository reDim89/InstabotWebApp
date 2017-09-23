## InstaBot Web App

This is a simple <a href="http://gunicorn.org/"> Gunicorn and <a href="http://aiohttp.readthedocs.io/">aiohttp</a> web app to run <a href="https://github.com/LevPasha">Instabot by Lev Pasha</a>.

## How to run locally:

1) Download and install `Python` to your computer.

2) To install the project's dependencies, run command `pip install -r requirements.txt` (specify `pip2` or `pip3` if you have multiple versions of Python installed)

3) Download ZIP and extract

4) In command line type the following commands:

```
$ gunicorn app.main:app --bind localhost:8081 --worker-class aiohttp.worker.GunicornWebWorker

```

## How to deploy on Heroku:

Just connect your Heroku account to this repository.
