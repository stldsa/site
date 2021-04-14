import json
import shutil
from pathlib import Path
from typing import List

from django.conf import settings
from django.contrib.sites.models import Site
from django.core.management import call_command
from django.core.management.base import BaseCommand

PROJECT_USES_CMS = False

try:
    from wagtail.core.models import Page, PageRevision
    from wagtail.core.models import Site as WagtailSite

    PROJECT_USES_CMS = True
except ImportError:
    pass


class Command(BaseCommand):
    """Sets up initial project data & settings. Also in production!"""

    help = "Sets up initial project data & settings. Also in production!"

    def _set_domain(self):
        """Sets the django and wagtail domains.

        Across all environments.
        """
        current_site = Site.objects.get_current()
        if settings.DEBUG:
            current_site.domain = "localhost:3000"
            current_site.name = "localhost dev"
        elif getattr(settings, "STAGING", False):
            current_site.domain = "test.codista.com"
            current_site.name = "test.codista.com"
        else:
            current_site.domain = "www.codista.com"
            current_site.name = "www.codista.com"
        current_site.save()
        if PROJECT_USES_CMS:
            wagtail_site = WagtailSite.objects.get()
            wagtail_site.hostname = current_site.domain
            wagtail_site.site_name = current_site.name
            wagtail_site.save()

    def setup_production(self):
        """PRODUCTION ONLY STUFF."""
        self._set_domain()
        call_command("create_project_users", verbosity=self.verbosity)

    def setup_development(self):
        """DEVELOPMENT ONLY STUFF."""
        self.setup_production()

    def handle(self, *args, **options):
        """entry point"""
        self.verbosity = options["verbosity"]
        if not settings.DEBUG:
            if self.verbosity > 0:
                self.stdout.write("Setting up production defaults...")
            self.setup_production()
            return

        if self.verbosity > 0:
            self.stdout.write("Setting up sensible development defaults...")
        self.setup_development()
