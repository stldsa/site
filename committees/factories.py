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
    name = fake("word")
    description = fake("paragraph")
    formation_type = fake("random_element", elements={"CT", "WG", "CU", "PR"})
    slug = fake("word")
    email = fake("email")
    show_in_menus = True
    # parent = PostGeneration(
    #     lambda obj, create, extracted, **kwargs: parent.add_child(obj)
    # )
