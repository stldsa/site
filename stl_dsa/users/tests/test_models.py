import pytest
from stl_dsa.users.tests.factories import UserFactory
from django.contrib.auth.models import Group
from committees.models import CommitteePage

# TODO: This test needs to grant the group admin access in Wagtail to pass
# @pytest.mark.django_db
# def test_formation_leaders_wagtail_access():
#     user = UserFactory()
#     leader_group, _ = Group.objects.get_or_create(name="Formation Leaders")
#     user.groups.set([leader_group])
#     assert user.has_perm("wagtailadmin.access_admin")


@pytest.mark.django_db
def test_superuser_has_wagtail_access(admin_user):
    admin_user.has_perm("wagtailadmin.access_admin")
