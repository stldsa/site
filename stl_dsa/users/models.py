from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.urls import reverse
from django.utils.translation import ugettext_lazy as _
from django.db import models


class User(AbstractUser):

    # First Name and Last Name do not cover name patterns
    # around the globe.
    username = models.CharField(null=True, blank=True, max_length=150)
    first_name = models.CharField(null=False, blank=False, max_length=30)
    last_name = models.CharField(null=False, blank=False, max_length=30)
    email = models.EmailField(null=False, blank=False)

    def get_absolute_url(self):
        return reverse("users:detail", kwargs={"id": self.pk})

    def __str__(self):
        return str(self.first_name) + " " + str(self.last_name)
