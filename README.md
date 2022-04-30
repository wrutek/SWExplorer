# SWExplorer #

This is a small, training app for exploring data from SWAPI.

## Running ##

I recommend to use python virtualenv and python 3.10.
To run the app, you need to install the dependencies:

```bash
pip install -r requirements.txt
```
and for the dev requirements:

```bash
pip install -r requirements-dev.txt
```

You should also run the migrations:

```bash
python manage.py migrate
```

Then you can run the app:

```bash
./manage.py runserver
```

App will be available under ```http://localhost:8000```.

## DB ##

As it is training app, it is using sqlite3 database.

## Testing ##

To run test just invoke:

```bash
pytest
```

