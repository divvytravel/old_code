sormcrew
==============================

yacht journeys

Deployment
----------

Used [makesite](https://github.com/klen/makesite) utility.
Look [makesite docs](http://pythonhosted.org/makesite/) for details.
In short, to update a project:

 - push to repo
 - on server, run `makesite update masstravel`


Run this script: (TODO - automate this)

.. code-block:: python

    from django.contrib.sites.models import Site
    site = Site.objects.get()
    site.domain = "masstravel.com"
    site.name = "masstravel"
    site.save()


Load cities and countries
-------------------------

    python manage.py init_geo


I18N processing
---------------

    python manage.py makemessages -l ru --settings=config.settings
    python manage.py compilemessages --settings=config.settings


Helpers
-------

Create fixtures:

    python manage.py dumpdata --indent=4 > initial_data.json


GeoIP
-----

put GeoLiteCity.dat into settings.GEOIP_PATH


Client code compilation
-----------------------
Requirements: nodejs > 0.10, npm

.. code-block:: bash
  npm install -g gulp
  npm install
  gulp build --target ../divvy/static/

  # load fixtures
  sudo python manage.py loaddata ./../public/src/fixtures/users.json
  sudo python manage.py loaddata ./../public/src/fixtures/geo.json
  sudo python manage.py loaddata ./../public/src/fixtures/trips.json
