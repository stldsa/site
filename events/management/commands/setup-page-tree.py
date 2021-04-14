import json
import logging
from pathlib import Path

from django.apps import apps
from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.files import File
from django.core.management.base import BaseCommand
from wagtail.core.models import Page
from wagtail.images.models import Image

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
        # self._setup_language_redirection()
        self._setup_home()
        # self._setup_team_member_index()
        # self._setup_team_member_pages()
        # finally, create the menus
        # self._create_main_menu()
        # self._create_flat_menus()

    def _set_image(self, obj, attr_name, folder_path, img_path):
        """helper to set images for objects"""
        img_path = folder_path.joinpath(img_path)
        # create and set the file if it does not yet exist
        qs = Image.objects.filter(title=img_path.name)
        if not qs.exists():
            with open(img_path, "rb") as f:
                # setting name= is important. otherwise it uses the entire file path as
                # name, which leaks server filesystem structure to the outside.
                image_file = File(f, name=img_path.stem)
                image = Image(title=img_path.name, file=image_file.open())
                image.save()
        else:
            image = qs[0]
        setattr(obj, attr_name, image)
        obj.save()

    def _setup_language_redirection(self):
        """First things first, tear down the dummy root page.
        and setup our language_redirection page
        """
        ContentType = apps.get_model("contenttypes.ContentType")
        Page = apps.get_model("wagtailcore.Page")
        Site = apps.get_model("wagtailcore.Site")
        LanguageRedirectionPage = apps.get_model("cms.LanguageRedirectionPage")
        # Delete the default homepage created by wagtail migrations If migration is run
        # multiple times, it may have already been deleted
        Page.objects.filter(id=2).delete()
        # Get content type for LanguageRedirectionPage model
        language_redirection_page_content_type = ContentType.objects.get(
            model="languageredirectionpage", app_label="cms"
        )
        # Create the base language redirection page which is responsible to redirect
        # the user to the language specific home pages
        root = Page.get_first_root_node()
        language_redirection_page = LanguageRedirectionPage(
            title="codista.com",
            draft_title="codista.com",
            slug="root",
            content_type=language_redirection_page_content_type,
            show_in_menus=True,
        )
        root.add_child(instance=language_redirection_page)

        # Create a site with the new LanguageRedirectionPage set as the root
        Site.objects.create(
            hostname="localhost",
            root_page=language_redirection_page,
            is_default_site=True,
            site_name="codista.com",
        )

    def _setup_home(self):
        """Creates the language specific home pages."""
        # LanguageRedirectionPage = apps.get_model("cms.LanguageRedirectionPage")
        # parent_page = LanguageRedirectionPage.objects.first()
        Page.objects.filter(id=2).delete()
        root = Page.get_first_root_node()

        Site = apps.get_model("wagtailcore.Site")
        # ContentType = apps.get_model("contenttypes.ContentType")
        HomePage = apps.get_model("home.HomePage")
        # homepage_content_type = ContentType.objects.get(
        #     model="homepage", app_label="home"
        # )
        # For each supported language, create a new homepage
        # for language_code, label in settings.LANGUAGES:
        #     if language_code == "de":
        #         hero_title = "Wir sind Codista."
        #         hero_intro = "Eine Software-Agentur, die sich auf die partnerschaftliche Entwicklung von hochqualitativen, digitalen Produkten spezialisiert hat."
        #         title = "Home - Deutsch"
        #         services_teaser = "Wir sind spezialisiert auf die Entwicklung von innovativen Software-Lösungen.  Mit langjähriger Erfahrung in Entwicklung und Design von Websites, Online-Plattformen,  Web-Applikationen und SaaS Lösungen unterstützen wir Ihr Unternehmen in der Realisierung neuer Software-Produkte und der Verbesserung Ihrer Unternehmens-Prozesse."
        #         services_title = "Wir denken digital."
        #         team_teaser = "Wir sind ein eingespieltes Team aus Software-Entwicklungs Experten und Design Profis welches komplexe Web-Projekte für unsere Kunden realisiert. Wir stehen für Qualität, Innovation, Umsetzungsgeschwindigkeit, Zuverlässigkeit und lösungsorientiertes Handeln."
        #         team_title = "Wir sind ein eingespieltes Team aus Software-Entwicklungs Experten und Design Profis."
        #         team_teaser = "Wir stehen für Qualität, Innovation, Umsetzungsgeschwindigkeit, Zuverlässigkeit und lösungsorientiertes Handeln."
        # elif language_code == "en":
        title = "Home - English"
        hero_title = "We are Codista."
        hero_intro = "A software agency specializing in the partnership development of high quality digital products."
        services_teaser = "We specialize in the development of innovative software solutions. With many years of experience in the development and design of websites, online platforms, web applications and SaaS solutions, we support your company in the realization of new software products and the improvement of your business processes."
        services_title = "We think digitally."
        team_title = "We are a well-established team of software development experts and design professionals."
        team_teaser = "We stand for quality, innovation, speed of implementation, reliability and solution-oriented action."
        # else:
        #     raise RuntimeError(f"unsupported language encountered: {language_code}")
        homepage = HomePage(
            # language=language_code,
            title="St Louis DSA",
            banner_title="We are the St. Louis Democratic Socialists of America!",
            body="Lorem Ipsum blah blah blah",
            # draft_title=title,
            # slug=language_code,
            # hero_title=hero_title,
            # hero_intro=hero_intro,
            # services_teaser=services_teaser,
            # services_title=services_title,
            # team_title=team_title,
            # team_teaser=team_teaser,
            # show_in_menus=True,
            # content_type=homepage_content_type,
        )
        root.add_child(instance=homepage)

    def _setup_contact_page(self):
        """Creates the contact page."""
        HomePage = apps.get_model("cms.HomePage")
        ContactPage = apps.get_model("cms.ContactPage")
        ContentType = apps.get_model("contenttypes.ContentType")
        contact_page_content_type = ContentType.objects.get(
            model="contactpage", app_label="cms"
        )
        home_page_de = HomePage.objects.get(language="de")
        contact_page_de = ContactPage(
            title="Kontakt",
            draft_title="Kontakt",
            slug="kontakt",
            hero_title="Los gehts.",
            hero_intro="Wir sind immer auf der Suche nach neuen Ideen und spannenden Projekten. Sagen Sie Hallo.",
            phone_number="+43 1 997 425 61 00",
            email="hello@codista.com",
            show_in_menus=True,
            content_type=contact_page_content_type,
        )
        home_page_de.add_child(instance=contact_page_de)
        home_page_en = HomePage.objects.get(language="en")
        contact_page_en = ContactPage(
            title="Contact",
            draft_title="Contact",
            slug="contact",
            hero_title="Lets go.",
            hero_intro="We are always on the hunt for new projects and interesting ideas! Say Hello.",
            phone_number="+43 1 997 425 61 00",
            email="hello@codista.com",
            show_in_menus=True,
            content_type=contact_page_content_type,
        )
        home_page_en.add_child(instance=contact_page_en)

        # connect these pages for translation
        contact_page_de.english_link = contact_page_en
        contact_page_de.save()

    def _setup_team_member_index(self):
        """Creates the language specific team member index pages."""
        HomePage = apps.get_model("cms.HomePage")
        TeamMemberIndexPage = apps.get_model("cms.TeamMemberIndexPage")
        ContentType = apps.get_model("contenttypes.ContentType")
        team_member_index_page_content_type = ContentType.objects.get(
            model="teammemberindexpage", app_label="cms"
        )
        home_page_de = HomePage.objects.get(language="de")

        intro_de = "Wir sind eine Software-Agentur mit Sitz in Wien. Unser Büro ist in Gehweite zum Naschmarkt zu finden. Mit einem starken Fokus auf Innovation unterstützen wir Unternehmen bei der Entwicklung und Verbesserung digitaler Produkte."
        team_member_index_de = TeamMemberIndexPage(
            title="Team",
            draft_title="Team",
            slug="team",
            hero_title="Unser Team",
            hero_intro=intro_de,
            show_in_menus=True,
            content_type=team_member_index_page_content_type,
        )
        home_page_de.add_child(instance=team_member_index_de)
        home_page_en = HomePage.objects.get(language="en")

        intro_en = "We are a software agency based in Vienna. Our office is within walking distance to the Naschmarkt. With a strong focus on innovation, we help companies develop and enhance digital products."
        team_member_index_en = TeamMemberIndexPage(
            title="Team",
            draft_title="Team",
            slug="team",
            hero_title="Our team",
            hero_intro=intro_en,
            show_in_menus=True,
            content_type=team_member_index_page_content_type,
        )
        home_page_en.add_child(instance=team_member_index_en)

        # connect these pages for translation
        team_member_index_de.english_link = team_member_index_en
        team_member_index_de.save()

    def _setup_team_member_pages(self):
        """Creates the language specific team member pages."""
        HomePage = apps.get_model("cms.HomePage")
        TeamMemberPage = apps.get_model("cms.TeamMemberPage")
        TeamMemberIndexPage = apps.get_model("cms.TeamMemberIndexPage")
        ContentType = apps.get_model("contenttypes.ContentType")

        home_page_de = HomePage.objects.get(language="de")
        home_page_en = HomePage.objects.get(language="en")
        team_member_index_page_de = TeamMemberIndexPage.objects.descendant_of(
            home_page_de
        ).first()
        team_member_index_page_en = TeamMemberIndexPage.objects.descendant_of(
            home_page_en
        ).first()

        team_member_page_content_type = ContentType.objects.get(
            model="teammemberpage", app_label="cms"
        )

        about_de = "<p>Thomas ist Geschäftsführer von Codista. Er stellt sicher, dass unsere Projekte in höchster Qualität und in der vereinbarten Zeit geliefert werden. Für unsere Kunden arbeitet er als Software-Entwickler und im Projekt Management.</p>"
        team_member_tom_de = TeamMemberPage(
            title="Thomas Kremmel",
            draft_title="Thomas Kremmel",
            slug="thomas-kremmel",
            name="Mag. Thomas Kremmel",
            organisational_role="Geschäftsführer",
            about=about_de,
            content_type=team_member_page_content_type,
        )
        team_member_index_page_de.add_child(instance=team_member_tom_de)
        folder_path = FIXTURES_DIR.joinpath("img")
        self._set_image(
            obj=team_member_tom_de,
            attr_name="portrait",
            folder_path=folder_path,
            img_path="tom.jpg",
        )

        about_en = "<p>Thomas is managing director of Codista. He ensures that our projects are delivered in the highest quality and on time. He works for our customers as a software developer and in project management.</p>"
        team_member_tom_en = TeamMemberPage(
            title="Thomas Kremmel",
            draft_title="Thomas Kremmel",
            slug="thomas-kremmel",
            name="Mag. Thomas Kremmel",
            organisational_role="CEO",
            about=about_en,
            content_type=team_member_page_content_type,
        )
        team_member_index_page_en.add_child(instance=team_member_tom_en)
        team_member_tom_de.english_link = team_member_tom_en
        team_member_tom_de.save()
        self._set_image(
            obj=team_member_tom_en,
            attr_name="portrait",
            folder_path=folder_path,
            img_path="tom.jpg",
        )

        about_de = "<p>Luis ist unser Tech Lead. Egal ob für uns intern oder für unsere Kunden: er ist verantwortlich für die gesamte technische Architektur, den reibungslosen Betrieb und die Sicherheit. Die Zufriedenheit unserer Kunden ist ihm eines der wichtigsten Anliegen.</p>"
        team_member_luis_de = TeamMemberPage(
            title="Luis Nell",
            draft_title="Luis Nell",
            slug="luis-nell",
            name="Luis Nell, BSc.",
            organisational_role="Tech Lead",
            about=about_de,
            content_type=team_member_page_content_type,
        )
        team_member_index_page_de.add_child(instance=team_member_luis_de)
        folder_path = FIXTURES_DIR.joinpath("img")
        self._set_image(
            obj=team_member_luis_de,
            attr_name="portrait",
            folder_path=folder_path,
            img_path="luis.jpg",
        )

        about_en = "<p>Luis is our tech lead. Whether for us internally or for our customers: he is responsible for the entire technical architecture, smooth operation and security. The satisfaction of our customers is one of his most important concerns.</p>"
        team_member_luis_en = TeamMemberPage(
            title="Luis Nell",
            draft_title="Luis Nell",
            slug="luis-nell",
            name="Luis Nell, BSc.",
            organisational_role="CTO",
            about=about_en,
            content_type=team_member_page_content_type,
        )
        team_member_index_page_en.add_child(instance=team_member_luis_en)
        team_member_luis_de.english_link = team_member_luis_en
        team_member_luis_de.save()
        self._set_image(
            obj=team_member_luis_en,
            attr_name="portrait",
            folder_path=folder_path,
            img_path="luis.jpg",
        )

    def _create_main_menu(self):
        from wagtailmenus.conf import settings as wagtailmenu_settings
        from wagtail.core.models import Site

        HomePage = apps.get_model("cms.HomePage")
        ContactPage = apps.get_model("cms.ContactPage")
        ServiceOverviewPage = apps.get_model("cms.ServiceOverviewPage")
        ProjectIndexPage = apps.get_model("cms.ProjectIndexPage")
        TeamMemberIndexPage = apps.get_model("cms.TeamMemberIndexPage")
        site = Site.objects.all()[0]
        menu_model = wagtailmenu_settings.models.FLAT_MENU_MODEL

        # create the german footer
        main_menu_de, created = menu_model.objects.get_or_create(
            site=site, handle="main_menu_de", title="main_menu_de"
        )
        home_page_de = HomePage.objects.get(language="de")
        if not main_menu_de.get_menu_items_manager().exists():
            # create the menu items for each page needed
            item_manager = main_menu_de.get_menu_items_manager()
            item_class = item_manager.model
            item_list = []
            service_overview_page_de = ServiceOverviewPage.objects.descendant_of(
                home_page_de
            ).first()
            item_list.append(
                item_class(
                    menu=main_menu_de,
                    link_text="Leistungen",
                    link_page=service_overview_page_de,
                    sort_order=1,
                    allow_subnav=False,
                )
            )
            project_index_page_de = ProjectIndexPage.objects.descendant_of(
                home_page_de
            ).first()
            item_list.append(
                item_class(
                    menu=main_menu_de,
                    link_text="Projekte",
                    link_page=project_index_page_de,
                    sort_order=2,
                    allow_subnav=False,
                )
            )
            team_member_index_page_de = TeamMemberIndexPage.objects.descendant_of(
                home_page_de
            ).first()
            item_list.append(
                item_class(
                    menu=main_menu_de,
                    link_text="Team",
                    link_page=team_member_index_page_de,
                    sort_order=4,
                    allow_subnav=False,
                )
            )
            contact_page_de = ContactPage.objects.descendant_of(home_page_de).first()
            item_list.append(
                item_class(
                    menu=main_menu_de,
                    link_text="Kontakt",
                    link_page=contact_page_de,
                    sort_order=5,
                    allow_subnav=False,
                )
            )
            item_manager.bulk_create(item_list)

        main_menu_en, created = menu_model.objects.get_or_create(
            site=site, handle="main_menu_en", title="main_menu_en"
        )
        home_page_en = HomePage.objects.get(language="en")
        if not main_menu_en.get_menu_items_manager().exists():
            # create the menu items for each page needed
            item_manager = main_menu_en.get_menu_items_manager()
            item_class = item_manager.model
            item_list = []

            service_overview_page_en = ServiceOverviewPage.objects.descendant_of(
                home_page_en
            ).first()
            item_list.append(
                item_class(
                    menu=main_menu_en,
                    link_text="Services",
                    link_page=service_overview_page_en,
                    sort_order=1,
                    allow_subnav=False,
                )
            )
            project_index_page_en = ProjectIndexPage.objects.descendant_of(
                home_page_en
            ).first()
            item_list.append(
                item_class(
                    menu=main_menu_en,
                    link_text="Projects",
                    link_page=project_index_page_en,
                    sort_order=2,
                    allow_subnav=False,
                )
            )
            team_member_index_page_en = TeamMemberIndexPage.objects.descendant_of(
                home_page_en
            ).first()
            item_list.append(
                item_class(
                    menu=main_menu_en,
                    link_text="Team",
                    link_page=team_member_index_page_en,
                    sort_order=4,
                    allow_subnav=False,
                )
            )
            contact_page_en = ContactPage.objects.descendant_of(home_page_en).first()
            item_list.append(
                item_class(
                    menu=main_menu_en,
                    link_text="Contact",
                    link_page=contact_page_en,
                    sort_order=5,
                    allow_subnav=False,
                )
            )
            item_manager.bulk_create(item_list)

    def _create_flat_menus(self):
        from wagtailmenus.conf import settings as wagtailmenu_settings
        from wagtail.core.models import Site

        HomePage = apps.get_model("cms.HomePage")
        PrivacyPolicyPage = apps.get_model("cms.PrivacyPolicyPage")
        DefaultPage = apps.get_model("cms.DefaultPage")
        site = Site.objects.all()[0]
        menu_model = wagtailmenu_settings.models.FLAT_MENU_MODEL

        # create the german footer
        footer_de, created = menu_model.objects.get_or_create(
            site=site, handle="footer_de", title="footer_de"
        )
        home_page_de = HomePage.objects.get(language="de")
        if not footer_de.get_menu_items_manager().exists():
            # create the menu items for each page needed
            item_manager = footer_de.get_menu_items_manager()
            item_class = item_manager.model
            item_list = []

            data_protection_page_de = PrivacyPolicyPage.objects.descendant_of(
                home_page_de
            ).get(slug="datenschutz")
            item_list.append(
                item_class(
                    menu=footer_de,
                    link_text="Datenschutz",
                    link_page=data_protection_page_de,
                    sort_order=2,
                    allow_subnav=False,
                )
            )
            terms_page_de = DefaultPage.objects.descendant_of(home_page_de).get(
                slug="agb"
            )
            item_list.append(
                item_class(
                    menu=footer_de,
                    link_text="AGB",
                    link_page=terms_page_de,
                    sort_order=3,
                    allow_subnav=False,
                )
            )
            imprint_page_de = DefaultPage.objects.descendant_of(home_page_de).get(
                slug="impressum"
            )
            item_list.append(
                item_class(
                    menu=footer_de,
                    link_text="Impressum",
                    link_page=imprint_page_de,
                    sort_order=4,
                    allow_subnav=False,
                )
            )
            item_manager.bulk_create(item_list)

        footer_en, created = menu_model.objects.get_or_create(
            site=site, handle="footer_en", title="footer_en"
        )
        home_page_en = HomePage.objects.get(language="en")
        if not footer_en.get_menu_items_manager().exists():
            # create the menu items for each page needed
            item_manager = footer_en.get_menu_items_manager()
            item_class = item_manager.model
            item_list = []

            data_protection_page_en = PrivacyPolicyPage.objects.descendant_of(
                home_page_en
            ).get(slug="privacy-policy")
            item_list.append(
                item_class(
                    menu=footer_en,
                    link_text="Privacy",
                    link_page=data_protection_page_en,
                    sort_order=2,
                    allow_subnav=False,
                )
            )
            terms_page_en = DefaultPage.objects.descendant_of(home_page_en).get(
                slug="terms"
            )
            item_list.append(
                item_class(
                    menu=footer_en,
                    link_text="Terms",
                    link_page=terms_page_en,
                    sort_order=3,
                    allow_subnav=False,
                )
            )
            imprint_page_en = DefaultPage.objects.descendant_of(home_page_en).get(
                slug="imprint"
            )
            item_list.append(
                item_class(
                    menu=footer_en,
                    link_text="Imprint",
                    link_page=imprint_page_en,
                    sort_order=4,
                    allow_subnav=False,
                )
            )
            item_manager.bulk_create(item_list)

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
