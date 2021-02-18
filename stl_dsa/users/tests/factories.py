from typing import Any, Sequence
from django.contrib.auth import get_user_model
from factory import django, post_generation
from faker import Faker

faker = Faker()
User = get_user_model()


class UserFactory(django.DjangoModelFactory):

    email = faker.email()
    first_name = faker.first_name()
    last_name = faker.last_name()

    @post_generation
    def password(self, create: bool, extracted: Sequence[Any], **kwargs):
        password = (
            extracted
            if extracted
            else faker.password(
                length=42,
                special_chars=True,
                digits=True,
                upper_case=True,
                lower_case=True,
            )
        )
        self.set_password(password)

    class Meta:
        model = User
