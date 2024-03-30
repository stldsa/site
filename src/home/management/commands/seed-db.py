import datetime
import logging
from pathlib import Path
from faker import Faker
from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from django.core.files.images import ImageFile
from wagtail.models import Page, Site
from wagtail.images.models import Image
from events.models import Event
from home.models import HomePage, JoinPage
from news.models import NewsIndexPage, InfoPage, NewsPageRelatedStory
from about.models import ExecutiveCommitteePage, BylawsPage
from committees.models import FormationsPage, CommitteePage
from django.contrib.auth.models import Group

fake = Faker()

User = get_user_model()

logger = logging.getLogger("setup_page_tree")


class Command(BaseCommand):
    """
    this command is used to create the initial wagtail cms page tree
    """

    help = "creates initial wagtail cms page tree"

    def _setup(self):
        Page.objects.filter(id=2).delete()
        root = Page.get_first_root_node()
        if root:
            homepage = HomePage(
                title="St Louis DSA",
                highlighted_campaign=f"{' '.join(fake.words(2)).title()} Campaign",
                highlighted_description=fake.paragraph(5),
            )
            root.add_child(instance=homepage)
            site = Site(
                hostname="localhost",
                root_page=homepage,
                is_default_site=True,
                site_name="stldsa.org",
            )
            site.save()

            joinpage = JoinPage(title="Join", slug="join", description=fake.paragraph())
            homepage.add_child(instance=joinpage)

            newsindexpage = NewsIndexPage(
                title="Updates",
                slug="updates",
            )
            homepage.add_child(instance=newsindexpage)
            aboutuspage = InfoPage(title="About Us", slug="about-us")
            homepage.add_child(instance=aboutuspage)
            ecpage = ExecutiveCommitteePage(
                title="Executive Committee", slug="ec", description=fake.paragraph()
            )
            aboutuspage.add_child(instance=ecpage)
            bylawspage = BylawsPage(
                title="Bylaws", slug="bylaws", description="Bylaws of the chapter."
            )
            aboutuspage.add_child(instance=bylawspage)

            NewsPage = apps.get_model("news.NewsPage")

            def add_news_page():
                newspage = NewsPage(
                    title=fake.sentence(),
                    first_published_at=fake.date_time(),
                    stories=[
                        NewsPageRelatedStory(
                            title=fake.sentence(),
                            description=fake.paragraph(),
                        )
                        for _ in range(4)
                    ],
                )
                newsindexpage.add_child(instance=newspage)

            for _ in range(5):
                add_news_page()

            formations_page = FormationsPage(
                title="Formations", description=fake.paragraphs()
            )
            homepage.add_child(instance=formations_page)

            committees = {
                "CT": [
                    "Communications",
                    "Community",
                    "Labor",
                    "Political Education",
                    "Tech",
                ],
                "WG": ["Electoral", "Socialist Feminist", "Housing Justice"],
                "CU": ["Afrosocialists & Socialists of Color"],
            }

            def add_committee_page(title, formation_type):
                committee_page = CommitteePage(
                    title=title,
                    description=fake.paragraph(),
                    formation_type=formation_type,
                    email=fake.email(),
                )
                formations_page.add_child(instance=committee_page)

            for formation_type, committees in committees.items():
                for committee in committees:
                    add_committee_page(committee, formation_type)

            future_event = Event.objects.create(
                title="New Member Orientation",
                description=fake.paragraph(),
                start=fake.future_datetime(
                    end_date=datetime.timedelta(days=6),
                    tzinfo=datetime.timezone.utc,
                ),
            )
            future_event.save()
            future_event_2 = Event(
                title="Monthly Drop-In",
                description=fake.paragraph(),
                start=fake.future_datetime(
                    end_date=datetime.timedelta(days=6),
                    tzinfo=datetime.timezone.utc,
                ),
            )
            future_event_2.save()
            formations_page.save()

            members = Group.objects.create(name="Members")

            member = User.objects.create(
                username="member@example.com",
                password="member",
            )

            member.groups.add(members)

    def handle(self, raise_error=False, *args, **options):
        # Root Page and a default homepage are created by wagtail migrations
        # so check for > 2 here
        verbosity = options["verbosity"]
        checks = [Page.objects.all().count() > 2]
        if any(checks):
            # YOU SHOULD NEVER RUN THIS COMMAND WITHOUT PRIOR DB DUMP
            print("Pages exist. Skipping Wagtail page generation.")
            return

        self._setup()
        if verbosity > 0:
            msg = "Page Tree successfully created."
            self.stdout.write(msg)
