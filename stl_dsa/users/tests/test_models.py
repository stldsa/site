import pytest
from stl_dsa.users.tests.factories import UserFactory
from django.contrib.auth.models import Group
from committees.models import CommitteePage


@pytest.mark.django_db
def test_is_member():
    member = UserFactory()
    member_group, _ = Group.objects.get_or_create(name="Members")
    member.groups.set([member_group])
    # nonmember = UserFactory()
    assert member.is_member
    # assert not nonmember.is_member


@pytest.mark.django_db
def test_formation_leaders_wagtail_access():
    user = UserFactory()
    leader_group, _ = Group.objects.get_or_create(name="Formation Leaders")
    user.groups.set([leader_group])
    assert user.has_perm("wagtailadmin.access_admin")


@pytest.mark.django_db
def test_superuser_has_wagtail_access(admin_user):
    admin_user.has_perm("wagtailadmin.access_admin")
