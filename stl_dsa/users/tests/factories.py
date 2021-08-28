from django.contrib.auth import get_user_model
from factory import django, post_generation, Sequence
from faker import Faker

faker = Faker()
User = get_user_model()


class UserFactory(django.DjangoModelFactory):
    class Meta:
        model = User

    class Params:
        is_member = False

    email = faker.email()
    first_name = faker.first_name()
    last_name = faker.last_name()
    id = Sequence(lambda n: str(n))

    @post_generation
    def groups(self, create, extracted, **kwargs):
        if extracted and create:
            self.groups.add(extracted)

    @post_generation
    def password(self, create, extracted, **kwargs):
        password = extracted or faker.password()
        self.set_password(password)
