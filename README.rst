stormcrew
==============================

yacht journeys


LICENSE: BSD

Deployment
------------

TODO

Run this script: (TODO - automate this)

.. code-block:: python

    from django.contrib.sites.models import Site
    site = Site.objects.get()
    site.domain = "stormcrew.ru"
    site.name = "stormcrew"
    site.save()

I18N processing
---------------

    python manage.py makemessages -l ru --settings=config.settings
    python manage.py compilemessages --settings=config.settings
