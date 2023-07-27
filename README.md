# Open Flask API
A lightweight RESTful API template based on Flask, which supports Python 2.7 and 3.6+

## Project Structure

### `api.lib` - Main App Library
This framework is designed with the Model-View-Controller pattern, hence `api.lib` is the controller of this application.
### `api.models` - ORMs
Per name, ORM database models should be located under this directory. This project uses `sqlalchemy` to implement models. For instance, `api.models.your_app.hello` has a model `Hello` which binds to database table `hello`.

### `api.views` - Views for API
This directory hosts all API entries of the application. Upon starting, all files under `api/views/*` are scanned for subclass of `APIView` and to have those subclasses registered as API entries. E.g. `api.views.your_app.hello.py` implements `HelloWorldView` class which inherents the class `APIView` and it shall be registered onto the entry point `/api/v0.1/hello` 

### `api.tasks` - Celery Tasks
Celery is used for implementing tasks in this project, and all tasks related code shall be located in `api.tasks`.

### `api.commands` - Command Line Tools
Besides the running RESTful API, this project implements command line tools using Click and has them integrated in the flask app. Any functions in `api.commands.*` decorated with `@click.command()` is registered under its name in cabab-case as click command and they should be run like `flask your-command-name`


## Environment Configuration
It is recommended to use `pipenv` for environment configuration and management for this project. A virtualenv will be automatically created upon the initial activation of pipenv for the project directory.

#### Activate pipenv virtual environment
```
pipenv shell
```

#### Install Requirements
```
pipenv install
```

This will install requirements in `Pipfile`

#### Environmental Variables

A `.env` file is provided for environmental variable settings which contains some settings for the project. Please make sure the `SECRET_KEY` is set up properly before continue.


## Run the Project

#### Settings File
Before run the project, make sure you have a `settings.py` under current directory and an example settings file is provided.

```
cp settings.example.py settings.py
```

#### Flask App
To run the RESTful API, use the following command. The RESTful API will by default serve at `http://127.0.0.1:5000/api/v0.1/`

```
flask run
```

#### Celery Tasks
To run the celery tasks, use the following command.

```
celery celery_worker.celery worker --concurrency=2 -E -Q {queue name} --logfile={queue name}.log --pidfile={queue name}.pid -D
```

#### Command Line Tools

```
flask what-ever-command
```




## TL;DR
First clone the project and to the following.
### Install Dependency
```
pipenv shell
pipenv install
cp settings.example.py settings.py
```
### Start Project
```
flask run
```
Visit http://127.0.0.1:5000/api/v0.1/hello
