from django.db import models
from wagtail.models import Page, Orderable
from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel, InlinePanel
from modelcluster.fields import ParentalKey


class Officers(Orderable):
    page = ParentalKey(
        "about.ExecutiveCommitteePage",
        on_delete=models.CASCADE,
        related_name="executive_committee",
    )

    Offices = models.IntegerChoices(
        "Office",
        (
            "CO_CHAIRS TREASURER CORRESPONDING_SECRETARY "
            "RECORDING_SECRETARY COMRADES_AT_LARGE",
        ),
    )
    position = models.IntegerField(choices=Offices.choices)
    person = models.CharField(max_length=50, null=True, blank=True)
    description = models.TextField()
    email = models.EmailField(null=True, blank=True)


class ExecutiveCommitteePage(Page):
    description = RichTextField()

    content_panels = [
        FieldPanel("title"),
        FieldPanel("description"),
        InlinePanel("executive_committee", heading="Executive Committee"),
    ]
