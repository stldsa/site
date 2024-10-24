from committees.models import CommitteePage
from wagtail.signals import page_published
from django.dispatch import receiver
from django.contrib.auth.models import Group


@receiver(page_published, sender=CommitteePage)
def handler(sender, **kwargs):
    instance = kwargs["instance"]
    Group.objects.get_or_create(
        name=f"{instance.title} {instance.get_formation_type_display()} Chair(s)"
    )
