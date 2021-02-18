from typing import Any, Sequence

from stl_dsa.users.models import User
from factory import django, post_generation
from faker import Faker

faker = Faker()


class UserFactory(django.DjangoModelFactory):

    username = faker.email()
    first_name = faker.first_name()
    last_name = faker.last_name()

    # @post_generation
    # def password(self, create: bool, extracted: Sequence[Any], **kwargs):
    #     password = (
    #         extracted
    #         if extracted
    #         else faker.password(
    #             length=42,
    #             special_chars=True,
    #             digits=True,
    #             upper_case=True,
    #             lower_case=True,
    #         ).generate(extra_kwargs={})
    #     )
    #     self.set_password(password)

    class Meta:
        model = User
