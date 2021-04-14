from django.db.models.fields import CharField
import requests
from datetime import datetime
from django.db import models
from stl_dsa.users.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save
from django.dispatch import receiver
from wagtail.core.models import Page
from wagtail.core.fields import RichTextField
from wagtail.snippets.models import register_snippet
from wagtail.admin.edit_handlers import FieldPanel
from wagtail.search import index

# Create your models here.


class Person(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)
    phone = PhoneNumberField(null=True, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Person.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.person.save()

    def __str__(self):
        return self.user.first_name + " " + self.user.last_name

    @property
    def anonymous_name(self):
        return self.user.first_name + " " + self.user.last_name[:1] + "."


class Committee(models.Model):
    name = CharField(max_length=255)


class CommitteePage(Page):
    parent_page_types = ["CommitteesPage"]
    subpage_types = []

    COMMITTEE = "CT"
    WORKING_GROUP = "WG"
    CAUCUS = "CU"
    PRIORITY = "PR"
    FORMATION_CHOICES = [
        (COMMITTEE, "Committee"),
        (WORKING_GROUP, "Working Group"),
        (CAUCUS, "Caucus"),
        (PRIORITY, "Priority"),
    ]

    name = models.CharField(max_length=30)
    description = RichTextField()
    formation_type = models.CharField(
        max_length=2, choices=FORMATION_CHOICES, default=""
    )
    leader = models.ForeignKey(
        Person,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="committee_leader",
    )
    leader_name = models.CharField(max_length=30)
    email = models.EmailField()
    people = models.ManyToManyField(Person, related_name="committee_member", blank=True)
    api_key = models.CharField(max_length=32, null=True, blank=True)
    sign_up_form_endpoint = models.TextField(null=True, blank=True)

    search_fields = Page.search_fields + [index.SearchField("description")]

    content_panels = Page.content_panels + [
        FieldPanel("name"),
        FieldPanel("description"),
        FieldPanel("formation_type"),
        FieldPanel("leader_name"),
        FieldPanel("email"),
        FieldPanel("sign_up_form_endpoint"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        embeds = requests.get(
            f"{self.sign_up_form_endpoint}/embed",
            headers={"OSDI-API-Token": self.api_key},
        ).json()
        embed_code = embeds["embed_standard_layout_only_styles"]
        context["embed_code"] = embed_code

        events_response = requests.get(
            "https://actionnetwork.org/api/v2/events",
            headers={"OSDI-API-Token": self.api_key},
        ).json()
        events_list = events_response["_embedded"]["osdi:events"]
        upcoming_events = []
        for event in events_list:
            event_date = datetime.fromisoformat(event["start_date"][:-1]).date()
            if event_date >= datetime.now().date() and event["status"] == "confirmed":
                event["date"] = event_date
                event["start_time"] = datetime.fromisoformat(
                    event["start_date"][:-1]
                ).time()
                upcoming_events.append(event)
        context["upcoming_events"] = upcoming_events

        return context


class CommitteesPage(Page):
    parent_page_types = []
    subpage_types = ["CommitteePage"]

    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        committees = CommitteePage.objects.all().order_by("title")
        context["committees"] = committees

        return context