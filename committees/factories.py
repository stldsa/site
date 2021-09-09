from factory.declarations import LazyAttribute
from factory.django import DjangoModelFactory
from factory import Faker as fake


class FormationsPageFactory(DjangoModelFactory):
    class Meta:
        model = "committees.CommitteesPage"

    title = "What We Do"
    slug = "formations"


class CommitteeFactory(DjangoModelFactory):
    class Meta:
        model = "committees.CommitteePage"

    class Params:
        parent = None

    title = fake("word")
    description = fake("paragraph")
    formation_type = fake("random_element", elements={"CT", "WG", "CU", "PR"})
    slug = LazyAttribute(lambda o: o.title)
    email = fake("email")
    show_in_menus = True
    leader_name = fake("name")
