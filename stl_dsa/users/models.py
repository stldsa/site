from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from actionnetwork.action_network import Person, People, Taggings
from django.contrib.auth.models import Group

VOTING_MEMBER_TAG_ID = "7cb02320-3ecc-4479-898e-67769a1bf7be"


class UserManager(BaseUserManager):
    def create_user(self, email, first_name=None, last_name=None, password=None):
        """
        Creates and saves a User with the given email, date of
        birth and password.
        """
        if not email:
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(email),
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        """
        Creates and saves a superuser with the given email, date of
        birth and password.
        """
        user = self.create_user(
            email,
            password=password,
        )
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    # First Name and Last Name do not cover name patterns
    # around the globe.
    # username = models.CharField(null=True, blank=True, max_length=150)
    first_name = models.CharField(null=True, blank=False, max_length=30)
    last_name = models.CharField(null=True, blank=False, max_length=30)
    email = models.EmailField(null=False, blank=False, unique=True)
    uuid = models.UUIDField(null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_member = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    @property
    def actionnetwork_people(self):
        return People.from_email(self.email).ids

    def get_uuid(self):
        uuid = self.actionnetwork_people[0]
        self.uuid = uuid
        return uuid

    @property
    def taggings(self):
        return Taggings(self.uuid or self.get_uuid())

    @property
    def is_member(self):
        return self.taggings.has_tag(VOTING_MEMBER_TAG_ID)

    def update_model_from_api(self):
        new_people = People.from_email(self.email)

    def update_membership(self):
        member_group = Group.objects.get(name="Members")
        if self.is_member:
            self.groups.add(member_group)
        else:
            self.groups.remove(member_group)

    def __str__(self):
        return f"{str(self.first_name)} {str(self.last_name)}"
