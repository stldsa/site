import datetime
import logging
from faker import Faker
from pathlib import Path
from django.conf import settings
from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.management.base import BaseCommand
from wagtail.core.models import Page
from wagtail.images.models import Image
from events.models import Event

fake = Faker()

User = get_user_model()

APP_DIR = Path(__file__).resolve().parent.parent.parent
FIXTURES_DIR = APP_DIR.joinpath("fixtures")

logger = logging.getLogger("setup_page_tree")


class Command(BaseCommand):
    """
    this command is used to create the initial wagtail cms page tree
    """

    help = "creates initial wagtail cms page tree"
    requires_system_checks = False

    def _setup(self):
        Page.objects.filter(id=2).delete()
        root = Page.get_first_root_node()

        Site = apps.get_model("wagtailcore.Site")
        HomePage = apps.get_model("home.HomePage")
        homepage = HomePage(
            title="St Louis DSA",
            banner_title="We are the St. Louis Democratic Socialists of America!",
            body="<h3>Our Mission:</h3><p><b>Create a more equitable world by establishing socialism as a political force</b></p><h3>We Believe:</h3><p><b>Our government and economy should operate, through social ownership, for the benefit of all</b></p>",
        )
        root.add_child(instance=homepage)
        site = Site(
            hostname="localhost",
            root_page=homepage,
            is_default_site=True,
            site_name="St Louis DSA",
        )
        site.save()
        NewsIndexPage = apps.get_model("news.NewsIndexPage")
        newsindexpage = NewsIndexPage(title="News", slug="news")
        homepage.add_child(instance=newsindexpage)
        NewsPage = apps.get_model("news.NewsPage")
        newspage = NewsPage(
            title="Today's News",
            slug="1",
            date=datetime.date.today(),
            body=fake.paragraph(),
        )
        newsindexpage.add_child(instance=newspage)
        future_event = Event(
            title="Event Title",
            description=fake.paragraph(),
            start=fake.future_datetime(tzinfo=datetime.timezone.utc),
        )
        future_event.save()

    def handle(self, raise_error=False, *args, **options):
        # Root Page and a default homepage are created by wagtail migrations
        # so check for > 2 here
        verbosity = options["verbosity"]
        checks = [Page.objects.all().count() > 2]
        if any(checks):
            # YOU SHOULD NEVER RUN THIS COMMAND WITHOUT PRIOR DB DUMP
            raise RuntimeError("Pages exists. Aborting.")

        self._setup()
        if verbosity > 0:
            msg = "Page Tree successfully created."
            self.stdout.write(msg)
