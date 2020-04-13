from django.db import models
from stl_dsa.users.models import User
from phonenumber_field.modelfields import PhoneNumberField
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Person(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.SET_NULL)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = PhoneNumberField()

    @receiver(post_save, sender=User)
    def create_user_profile(sender, instance, created, **kwargs):
        if created:
            Person.objects.create(user=instance)

    @receiver(post_save, sender=User)
    def save_user_profile(sender, instance, **kwargs):
        instance.person.save()

    def __str__(self):
        return self.first_name + ' ' + self.last_name

class Committee(models.Model):
    COMMITTEE = 'C'
    WORKING_GROUP = 'WG'
    FORMATION_CHOICES = [
        (COMMITTEE, 'Committee'),
        (WORKING_GROUP, 'Working Group'),
    ]
    name = models.CharField(max_length=30)
    description = models.TextField()
    slug = models.CharField(max_length=10, null=True)
    formation_type = models.CharField(max_length=2, choices=FORMATION_CHOICES, default='')
    leader = models.ForeignKey(Person, null=True, blank=True, on_delete=models.SET_NULL, related_name='committee_leader')
    people = models.ManyToManyField(Person, related_name='committee_member', blank=True)

    def __str__(self):
        return self.name # + ' ' + self.get_formation_type_display