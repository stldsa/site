import datetime
import logging
from faker import Faker
from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from wagtail.models import Page, Site
from events.models import Event
from home.models import HomePage, JoinPage
from news.models import NewsIndexPage, InfoPage, NewsPageRelatedStory
from about.models import ExecutiveCommitteePage, BylawsPage
from committees.models import CommitteesPage, FormationsPage, CommitteePage
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
            aboutuspage = InfoPage(title="About Us", slug="about")
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
            newspage = NewsPage(
                title=fake.sentence(),
                first_published_at=fake.date_time(),
                stories=[
                    NewsPageRelatedStory(
                        title=fake.sentence(), description=fake.paragraph()
                    )
                    for _ in range(4)
                ],
            )
            newsindexpage.add_child(instance=newspage)
            newspage2 = NewsPage(
                title=fake.sentence(), first_published_at=fake.date_time()
            )
            newsindexpage.add_child(instance=newspage2)

            newspage3 = NewsPage(
                title=fake.sentence(), first_published_at=fake.date_time()
            )
            newsindexpage.add_child(instance=newspage3)

            newspage4 = NewsPage(
                title=fake.sentence(), first_published_at=fake.date_time()
            )
            newsindexpage.add_child(instance=newspage4)

            newspage5 = NewsPage(
                title=fake.sentence(), first_published_at=fake.date_time()
            )
            newsindexpage.add_child(instance=newspage5)

            formations_page = FormationsPage(
                title="Formations", description=fake.paragraphs()
            )
            homepage.add_child(instance=formations_page)
            committees_page = CommitteesPage(
                title="Committees", description=fake.paragraph()
            )
            formations_page.add_child(instance=committees_page)
            working_groups_page = CommitteesPage(
                title="Working Groups", description=fake.paragraph()
            )
            formations_page.add_child(instance=working_groups_page)
            caucuses_page = CommitteesPage(
                title="Caucuses", description=fake.paragraph()
            )
            formations_page.add_child(instance=caucuses_page)
            priorities_page = CommitteesPage(
                title="Priority Groups", description=fake.paragraph(), live=False
            )
            formations_page.add_child(instance=priorities_page)

            communications_page = CommitteePage(
                title="Communications",
                description=fake.paragraph(),
                formation_type="CT",
                email=fake.email(),
                leader_name=fake.name(),
            )
            committees_page.add_child(instance=communications_page)

            community_page = CommitteePage(
                title="Community",
                description=fake.paragraph(),
                formation_type="CT",
                email=fake.email(),
                leader_name=fake.name(),
            )
            committees_page.add_child(instance=community_page)

            labor_page = CommitteePage(
                title="Labor",
                description=fake.paragraph(),
                formation_type="CT",
                email=fake.email(),
                leader_name=fake.name(),
            )
            committees_page.add_child(instance=labor_page)

            polied_page = CommitteePage(
                title="Political Education",
                description=fake.paragraph(),
                formation_type="CT",
                email=fake.email(),
                leader_name=fake.name(),
            )
            committees_page.add_child(instance=polied_page)

            tech_page = CommitteePage(
                title="Tech",
                description=fake.paragraph(),
                formation_type="CT",
                email=fake.email(),
                leader_name=fake.name(),
            )
            committees_page.add_child(instance=tech_page)

            electoral_page = CommitteePage(
                title="Electoral",
                description=fake.paragraph(),
                formation_type="WG",
                email=fake.email(),
                leader_name=fake.name(),
            )
            working_groups_page.add_child(instance=electoral_page)

            socfem_page = CommitteePage(
                title="Socialist Feminist",
                description=fake.paragraph(),
                formation_type="WG",
                email=fake.email(),
                leader_name=fake.name(),
            )
            working_groups_page.add_child(instance=socfem_page)

            housing_page = CommitteePage(
                title="Housing Justice",
                description=fake.paragraph(),
                formation_type="WG",
                email=fake.email(),
                leader_name=fake.name(),
            )
            working_groups_page.add_child(instance=housing_page)

            afrosoc_page = CommitteePage(
                title="Afrosocialists and Socialists of Color Caucus",
                description=fake.paragraph(),
                formation_type="CU",
                email=fake.email(),
                leader_name=fake.name(),
            )
            caucuses_page.add_child(instance=afrosoc_page)

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

            Group.objects.create(name="Members")

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
