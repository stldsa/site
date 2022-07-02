import django.dispatch

page_publish_scheduled = django.dispatch.Signal(providing_args=["instance", "revision"])
