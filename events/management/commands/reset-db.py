import psycopg2
from django.conf import settings
from django.core.management import call_command
from django.core.management.base import BaseCommand


DATABASE_CONNECTION_DETAILS = {}
for database, conn_details in settings.DATABASES.items():
    DATABASE_CONNECTION_DETAILS[database] = {
        key.lower().replace("name", "dbname"): value
        for key, value in conn_details.items()
        if value and key.lower() in ["name", "user", "password", "host", "port"]
    }


class Command(BaseCommand):
    """DEV ONLY: Dumps the entire DB and sets up everything anew."""

    help = "DEV ONLY: Dumps the entire DB and sets up everything anew."
    requires_system_checks = False

    def _terminate_db_connections(self, database):
        """Terminates the database connections to be able to drop the database"""
        conn_kwargs = DATABASE_CONNECTION_DETAILS[database]
        postgres_db_conn_kwargs = conn_kwargs.copy()
        postgres_db_conn_kwargs["dbname"] = "postgres"
        conn = psycopg2.connect(**postgres_db_conn_kwargs)
        conn.autocommit = True
        cur = conn.cursor()
        # DANGER: Not using prepared variables here. hardcore python formatting.
        cur.execute(
            "SELECT pg_terminate_backend(pg_stat_activity.pid) FROM pg_stat_activity WHERE pg_stat_activity.datname = '{}' AND pid <> pg_backend_pid();".format(
                conn_kwargs["dbname"]
            )
        )

    def _create_db(self, database):
        """Sets up the database"""
        conn_kwargs = DATABASE_CONNECTION_DETAILS[database]
        postgres_db_conn_kwargs = conn_kwargs.copy()
        postgres_db_conn_kwargs["dbname"] = "postgres"
        conn = psycopg2.connect(**postgres_db_conn_kwargs)
        conn.autocommit = True
        cur = conn.cursor()
        # DANGER: Not using prepared variables here. hardcore python formatting.
        cur.execute("CREATE DATABASE {};".format(conn_kwargs["dbname"]))

    def _drop_db(self, database):
        """Drops the database"""
        conn_kwargs = DATABASE_CONNECTION_DETAILS[database]
        postgres_db_conn_kwargs = conn_kwargs.copy()
        postgres_db_conn_kwargs["dbname"] = "postgres"
        conn = psycopg2.connect(**postgres_db_conn_kwargs)
        conn.autocommit = True
        cur = conn.cursor()
        # DANGER: Not using prepared variables here. hardcore python formatting.
        cur.execute("DROP DATABASE {};".format(conn_kwargs["dbname"]))

    def _create_or_recreate_db(self, database):
        """creates or recreates the database"""
        conn_kwargs = DATABASE_CONNECTION_DETAILS[database]
        try:
            psycopg2.connect(**conn_kwargs)
            self._drop_db(database)
            self._create_db(database)
        except psycopg2.OperationalError as e:
            if "does not exist" not in str(e):
                raise e
            self._create_db(database)

    def handle(self, *args, **options):
        """entry point"""
        verbosity = options["verbosity"]
        if not settings.DEBUG:
            # YOU SHOULD NEVER TRUST THIS COMMAND FOR PRODUCTION USAGE.
            raise RuntimeError("Command can not be run in production.")

        for database in settings.DATABASES.keys():
            self._terminate_db_connections(database)
            self._create_or_recreate_db(database)

        call_command("migrate", verbosity=verbosity)
        if verbosity > 0:
            self.stdout.write("Migrations done.")
        call_command("total_setup", verbosity=verbosity)

        # Total setup only creates content when there was a dump created by our
        # ``total_dump`` command.
        if verbosity > 0:
            msg = "Migrations done. Generating content. Time to grab a coffee..."
            self.stdout.write(msg)
        # this is a wagtail specific management command to setup some initial Wagtail pages
        # only needed if you are using Wagtail
        call_command("setup_page_tree", verbosity=verbosity)
