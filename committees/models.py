from django.db import models
from stl_dsa.users.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from wagtail import blocks
from wagtail.models import Page
from wagtail.fields import RichTextField, StreamField
from wagtail.admin.panels import FieldPanel
from wagtail.search import index
import requests


class Person(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.SET_NULL)
    phone = PhoneNumberField(null=True, blank=True)

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Person(user=instance).save()

    def __str__(self):
        if self.user:
            return (self.user.first_name or "") + " " + (self.user.last_name or "")


class CommitteePage(Page):
    parent_page_types = ["CommitteesPage"]

    COMMITTEE = "CT"
    WORKING_GROUP = "WG"
    CAUCUS = "CU"
    FORMATION_CHOICES = [
        (COMMITTEE, "Committee"),
        (WORKING_GROUP, "Working Group"),
        (CAUCUS, "Caucus"),
    ]

    description = RichTextField()
    image = models.ForeignKey(
        "wagtailimages.Image",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="+",
    )
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
    leaders = models.ManyToManyField(User)
    email = models.EmailField()
    people = models.ManyToManyField(Person, related_name="committee_member", blank=True)
    sign_up_form_endpoint = models.TextField(null=True, blank=True)

    search_fields = Page.search_fields + [index.SearchField("description")]

    content_panels = Page.content_panels + [
        FieldPanel("formation_type"),
        FieldPanel("description"),
        FieldPanel("image"),
        FieldPanel("leaders"),
        FieldPanel("email"),
        FieldPanel("sign_up_form_endpoint"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        if self.sign_up_form_endpoint:
            embeds = requests.get(
                f"{self.sign_up_form_endpoint}embed",
                headers={
                    "OSDI-API-Token": settings.ACTIONNETWORK_API_KEYS.get(self.slug)
                },
            ).json()
            embed_code = embeds.get("embed_standard_layout_only_styles")
        else:
            embed_code = None
        context["embed_code"] = embed_code
        context["formation_types"] = CommitteePage.objects.child_of(self).live()

        return context

    def __str__(self):
        return f"{self.title.title()} {self.get_formation_type_display()}"

    class Meta:
        verbose_name = "Formation"


class CommitteesPage(Page):
    subpage_types = ["CommitteePage"]
    description = RichTextField(null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("description"),
    ]

    def get_context(self, request):
        context = super().get_context(request)
        context["committees"] = self.objects.get_children().live().order_by("title")

        return context


class FormationsPage(Page):
    subpage_types = ["CommitteesPage"]
    description = RichTextField(null=True, blank=True)

    content_panels = Page.content_panels + [
        FieldPanel("description"),
    ]

    def get_context(self, request, *args, **kwargs):
        context = super().get_context(request, *args, **kwargs)
        formation_types = self.get_children().live().specific()
        for formation_type in formation_types:
            formation_type.formations = (
                formation_type.get_children().order_by("title").live().specific()
            )
        context["formation_types"] = formation_types
        return context


class ResourcesPage(Page):
    resources = StreamField(
        [
            (
                "resource",
                blocks.StreamBlock(
                    [
                        ("resource_name", blocks.CharBlock()),
                        ("information", blocks.RichTextBlock()),
                        (
                            "structured_info_block",
                            blocks.StreamBlock(
                                [
                                    ("heading", blocks.CharBlock()),
                                    ("body", blocks.RichTextBlock()),
                                ]
                            ),
                        ),
                    ]
                ),
            )
        ],
        use_json_field=True,
    )
    content_panels = Page.content_panels + [
        FieldPanel("resources"),
    ]
