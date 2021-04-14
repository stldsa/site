from events.models import Event
from rest_framework import serializers


class EventSerializer(serializers.HyperlinkedModelSerializer):
    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        return Response(queryset.values_list("state_name", flat=True))

    class Meta:
        model = Event
        fields = ("id", "title", "start", "url")
