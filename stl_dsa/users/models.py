from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
import actionnetwork.action_network as an
from django.contrib.auth.models import Group

VOTING_MEMBER_TAG_ID = "7cb02320-3ecc-4479-898e-67769a1bf7be"


class UserManager(BaseUserManager):
    def create_user(self, email, first_name=None, last_name=None, password=None):
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
        user = self.create_user(
            email,
            password=password,
        )
        user.is_superuser = True
        user.is_admin = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(null=True, blank=True, max_length=30)
    last_name = models.CharField(null=True, blank=True, max_length=30)
    email = models.EmailField(null=False, blank=False, unique=True)
    uuid = models.UUIDField(null=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin

    def get_uuid(self):
        ids = an.People(email=self.email).ids
        self.uuid = ids[0] if ids else None
        self.save()
        return self.uuid

    @property
    def membership_status(self):
        custom_fields = an.Person(self.uuid).custom_fields
        return (
            custom_fields.get("actionkit_is_member_in_good_standing")
            if custom_fields
            else None
        )

    @property
    def is_member(self):
        return self.membership_status

    def update_membership(self):
        member_group = Group.objects.get(name="Members")
        if self.is_member:
            self.groups.add(member_group)
        else:
            self.groups.remove(member_group)

    @property
    def is_leader(self):
        return "Leadership" in [group.name for group in list(self.groups.all())]

    def __str__(self):
        return self.email
