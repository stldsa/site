from factory.django import DjangoModelFactory
from wagtail.core.models import Page
from factory import Faker as fake
from factory import LazyAttribute


class PageFactory(DjangoModelFactory):
    class Meta:
        model = Page

    title = "St Louis DSA"
    slug = "en"


class HomePageFactory(DjangoModelFactory):
    class Meta:
        model = "home.HomePage"

    banner_title = "We are the St. Louis Democratic Socialists of America!"
    body = f"""
    <h3>Our Mission:</h3><p><b>{fake("sentence", nb_words=10)}</b></p><h3>We
    Believe:</h3><p><b>{fake("sentence", nb_words=10)}</b></p>
    """
    highlighted_campaign = LazyAttribute(
        lambda o: f"{' '.join(fake('words', nb=2)).title()} Campaign"
    )
    highlighted_description = fake("paragraph", nb=5)
