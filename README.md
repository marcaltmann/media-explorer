# Media Explorer

Research and presentation software for multimedia resources

## Wishlist

* API
* d3.js graphs

## Requirements

* Python 3.12
* Node.js 20
* Solr 9.x

## Installation

Create and or activate a Python virtual environment.

```shell
python -m venv .venv
source .venv/bin/activate
```

Install dependencies.

```shell
pip install -r requirements.txt
npm install
```

Start up Solr and create a new core. This assumes you have Solr installed already.

```shell
solr start
solr create -c media_explorer
```

Create test data and the Solr search index.

```shell
python manage.py migrate
python manage.py createtestdata
python manage.py createindex
```

## Start

Start the Django server.

```shell
python manage.py runserver
```

In a separate shell, start the Vite development server.

```shell
npm run dev
```

Now you can visit http://127.0.0.1:8000
