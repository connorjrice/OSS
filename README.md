
# OSS

A web framework written in Tornado utilizing a SQLITE backend to faciliate the ongoing operations of a martial arts gym.

This project is in prototype stage, but is a working concept of the design and architecture I will be using going forward.


## Getting Started

### Prerequisites
```
python 3.6+
```

### Installing

```
python setup.py install
python -m peak.server
connect to localhost:8000
```

### Structure
#### Astral
This is the backend of the webserver. It negotiates the ODBC connection and provides the logic for the web framework. It's built to be generic and extensible to other websites.

#### Notebooks
Jupyter notebooks for mocking up fake data in the database and interacting with them. I've found these notebooks to be incredibly useful for this type of task.

#### Peak
This is the actual implementation of the website. In some ways it's a submodule/implementation of Astral.

