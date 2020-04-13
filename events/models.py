from django.db import models

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    address = models.CharField(max_length=30, null=True, blank=True)
    city = models.CharField(max_length=30, null=True, blank=True)
    state = models.CharField(max_length=2, null=True, blank=True)
    zip = models.IntegerField(null=True, blank=True)
    description = models.TextField()
    actionnetwork_url = models.URLField()

    def __str__(self):
        return self.title + ' ' + str(self.date)


