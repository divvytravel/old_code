__author__ = 'indieman'

from django.db.models.signals import m2m_changed
from django.dispatch import receiver

from .models import Trip

@receiver(m2m_changed, sender=Trip.tags.through)
def set_tags(sender, instance, action, **kwargs):
    pass


@receiver(m2m_changed, sender=Trip.people.through)
def set_people(sender, instance, action, **kwargs):
    if action != "post_add":
        return None

    # create_for = Relationship.objects.filter(to_person__user__id__in=kwargs['pk_set']) \
    #     .values_list('from_person__user__id', flat=True)
    # create_for = list(set(create_for))
    #
    # for author_id in kwargs['pk_set']:
    #     try:
    #         create_for.remove(author_id)
    #     except ValueError:
    #         pass
    #
    # update_event_groups(
    #     event_type=EVENT_MOMENTS_ENTRY_FROM_FOLLOWING,
    #     content_object=instance,
    #     users=create_for,)
    #
    # if len(kwargs['pk_set']) == 1 and \
    #         not MomentsEntry.objects.filter(authors__id=kwargs['pk_set'][0]).exists():
    #     instance.content_description = "My #firstpost on Video Friends"
    #     hashtags, instance.content_description = self.moment.get_hashtags()
    #     instance.save()
    #     instance.hashtag = hashtags
