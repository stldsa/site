from django.conf import settings
from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand


User = get_user_model()
# some random team members generated via https://uinames.com/
USERS = [
    {
        "email": "lisa_fox@example.com",
        "first_name": "Lisa",
        "last_name": "Fox",
    },
    {
        "email": "johannes91@example.com",
        "first_name": "Johannes",
        "last_name": "Schwarz",
    },
    {
        "email": "vanessa_84@example.com",
        "first_name": "Vanessa",
        "last_name": "Werner",
    },
]


class Command(BaseCommand):
    """Creates project users.
    In development we simply set ``1234`` as password. In production we create users
    without valid passwords, so we can simply do a password reset procedure.
    """

    help = "Creates project users."
    requires_system_checks = False

    def handle(self, *args, **options):
        verbosity = options["verbosity"]
        admin_created = False
        if not User.objects.filter(email="admin@simpleloop.com").exists():
            User.objects.create_user("admin@simpleloop.com")
            admin_created = True
        if verbosity > 0:
            self.stdout.write("Admin created" if admin_created else "Admin exists.")

        for user_data in USERS:
            user_data = user_data.copy()
            email = user_data.pop("email")
            created = False
            created_user = None
            if not User.objects.filter(email=email).exists():
                created_user = User.objects.create_superuser(email, "1234", **user_data)
                created = True
            if verbosity > 0:
                self.stdout.write(
                    "{email} {noun}".format(
                        email=email, noun="created" if created else "exists"
                    )
                )
            #  When we run in production, make sure this command doesnt set 1234 as
            #  valid password lol.
            if not settings.DEBUG and created_user:
                # By using unusable password we get superusers which can then reset
                # their password.
                created_user.set_unusable_password()
                created_user.save()
                if verbosity > 0:
                    self.stdout.write("\tProduction run: set invalid password.")
