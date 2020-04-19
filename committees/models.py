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
        return self.user.first_name + ' ' + self.user.last_name

    @property
    def anonymous_name(self):
        return self.user.first_name + ' ' + self.user.last_name[:1] + '.'

# class Committee(models.Model):
#     COMMITTEE = 'C'
#     WORKING_GROUP = 'WG'
#     FORMATION_CHOICES = [
#         (COMMITTEE, 'Committee'),
#         (WORKING_GROUP, 'Working Group'),
#     ]
#     name = models.CharField(max_length=30)
#     # description = models.TextField()
#     slug = models.CharField(max_length=10, null=True)
#     formation_type = models.CharField(max_length=2, choices=FORMATION_CHOICES, default='')
#     leader = models.ForeignKey(Person, null=True, blank=True, on_delete=models.SET_NULL, related_name='committee_leader')
#     people = models.ManyToManyField(Person, related_name='committee_member', blank=True)
    
#     panels = [
#         FieldPanel('description'),
#     ]

#     def __str__(self):
#         return self.name # + ' ' + self.get_formation_type_display



class CommitteePage(Page):
    parent_page_types = ['CommitteesPage']
    subpage_types = []

    COMMITTEE = 'CT'
    WORKING_GROUP = 'WG'
    CAUCUS = 'CU'
    FORMATION_CHOICES = [
        (COMMITTEE, 'Committee'),
        (WORKING_GROUP, 'Working Group'),
        (CAUCUS, 'Caucus'),
    ]

    name = models.CharField(max_length=30)
    description = RichTextField()
    formation_type = models.CharField(max_length=2, choices=FORMATION_CHOICES, default='')
    leader = models.ForeignKey(Person, null=True, blank=True, on_delete=models.SET_NULL, related_name='committee_leader')
    leader_name = models.CharField(max_length=30)
    email = models.EmailField()
    people = models.ManyToManyField(Person, related_name='committee_member', blank=True)
    

    search_fields = Page.search_fields + [
        index.SearchField('description')
    ]

    content_panels = Page.content_panels + [
        FieldPanel('name'),
        FieldPanel('description'),
        FieldPanel('formation_type'),
        FieldPanel('leader_name'),
        FieldPanel('email')
    ]

class CommitteesPage(Page):
    parent_page_types = []
    subpage_types = ['CommitteePage']
    def get_context(self, request):
        # Update context to include only published posts, ordered by reverse-chron
        context = super().get_context(request)
        committees = CommitteePage.objects.all().order_by('title')
        context['committees'] = committees
        return context