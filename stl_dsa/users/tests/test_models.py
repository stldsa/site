import pytest
from stl_dsa.users.tests.factories import UserFactory
from django.contrib.auth.models import Group


@pytest.mark.django_db
def test_is_member():
    member = UserFactory()
    member_group, created = Group.objects.get_or_create(name="Members")
    member.groups.set([member_group])
    nonmember = UserFactory()
    assert member.is_member
    assert not nonmember.is_member
