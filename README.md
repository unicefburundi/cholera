Cholera
========================
App to monitor cholera outbreak.

Installation instructions
-------------------------

Below you will find basic setup instructions for the ``project_name``
project. To begin you should have the following applications installed on your
local development system:

- `Python >= 2.7`
- `pip >= 1.1 `
- `virtualenv >= 1.8 `

Getting Started
---------------

To setup your local environment you should create a virtualenv and install the necessary requirements:

    mkvirtualenv project_name-env


Then:

    cd project_name
    pip install -r requirements.txt

Run syncdb::

    python manage.py migrate sites
    python manage.py migrate auth
    python manage.py migrate authentication surveillance_cholera
    python manage.py migrate syncdb
    

You should now be able to run the development server:

    python manage.py runserver
