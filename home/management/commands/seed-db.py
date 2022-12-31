import datetime
import logging
from faker import Faker
import stringcase
from django.apps import apps
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand
from wagtail.models import Page, Site
from events.models import Event, EventsPage
from home.models import HomePage
from news.models import NewsIndexPage, InfoPage
from committees.models import CommitteesPage
from committees.factories import CommitteeFactory
from django.contrib.auth.models import Group

fake = Faker()

User = get_user_model()

logger = logging.getLogger("setup_page_tree")


committee_list = CommitteeFactory.build_batch(8)


class Command(BaseCommand):
    """
    this command is used to create the initial wagtail cms page tree
    """

    help = "creates initial wagtail cms page tree"

    def _setup(self):
        Page.objects.filter(id=2).delete()
        root = Page.get_first_root_node()
        homepage = HomePage(
            title="St Louis DSA",
            banner_title="Welcome to St Louis DSA!",
            mission_statement=fake.sentence(10),
            values_statement=fake.sentence(10),
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

        newsindexpage = NewsIndexPage(
            title="Updates",
            slug="updates",
            show_in_menus=True,
        )
        homepage.add_child(instance=newsindexpage)
        newsindexpage.has_children_in_menu = False
        newsindexpage.sub_menu = None

        NewsPage = apps.get_model("news.NewsPage")
        newspage = NewsPage(
            title=fake.sentence(),
            main_copy=fake.paragraph(10),
            show_in_menus=False,
        )
        newsindexpage.add_child(instance=newspage)
        newspage2 = NewsPage(
            title=fake.sentence(),
            main_copy=fake.paragraph(10),
            show_in_menus=False,
        )
        newsindexpage.add_child(instance=newspage2)

        event_menu_page = EventsPage(
            title="Events", show_in_menus=True, link_url="/events/"
        )
        homepage.add_child(instance=event_menu_page)
        formation_index = InfoPage(title="Formations", show_in_menus=True)
        homepage.add_child(instance=formation_index)
        for formation_type_name in [
            "Committees",
            "Working Groups",
            "Caucuses",
        ]:
            formation_type = CommitteesPage(
                title=formation_type_name,
                slug=stringcase.spinalcase(formation_type_name),
                show_in_menus=True,
            )
            formation_index.add_child(instance=formation_type)
            formation_list = CommitteeFactory.build_batch(4)
            for formation in formation_list:
                formation_type.add_child(instance=formation)
                revision = formation.save_revision()
                revision.publish()
                formation.save()

                future_event = Event.objects.create(
                    title="Event Title",
                    description=fake.paragraph(),
                    start=fake.future_datetime(
                        end_date=datetime.timedelta(days=6),
                        tzinfo=datetime.timezone.utc,
                    ),
                )
                future_event.save()
                future_event_2 = Event(
                    title="Event Title 2",
                    description=fake.paragraph(),
                    start=fake.future_datetime(
                        end_date=datetime.timedelta(days=6),
                        tzinfo=datetime.timezone.utc,
                    ),
                )
                future_event_2.save()

            revision = formation_type.save_revision()
            revision.publish()
            formation_type.save()
        formation_index.save()

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
