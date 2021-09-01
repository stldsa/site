from django.apps import AppConfig


class CommitteesConfig(AppConfig):
    name = "committees"

    def ready(self):
        import committees.signals.handlers  # noqa
