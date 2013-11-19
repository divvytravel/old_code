stormcrew
==============================

yacht journeys


LICENSE: BSD

Load cities and countries
-------------------------

    python manage.py init_geo


I18N processing
---------------

    python manage.py makemessages -l ru --settings=config.settings
    python manage.py compilemessages --settings=config.settings

Deployment
------------

TODO

Run this script: (TODO - automate this)

.. code-block:: python

    from django.contrib.sites.models import Site
    site = Site.objects.get()
    site.domain = "masstravel.ru"
    site.name = "masstravel"
    site.save()

Helpers
-------

Create fixtures:

    python manage.py dumpdata --indent=4 > initial_data.json
