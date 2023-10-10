from django.contrib.auth import get_user_model
from factory import django, post_generation, Sequence
from faker import Faker

faker = Faker()
User = get_user_model()


class UserFactory(django.DjangoModelFactory):
    class Meta:
        model = User

    email = Sequence(lambda n: f"person{n}@example.com")
    first_name = faker.first_name()
    last_name = faker.last_name()
    is_member = True

    @post_generation
    def password(
        self,
        _,
        extracted,
    ):
        password = extracted or faker.password()
        self.set_password(password)
