__author__ = 'indieman'

from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Trip

@receiver(m2m_changed, sender=Trip.tags.through)
def set_tags(sender, instance, action, **kwargs):
    pass
