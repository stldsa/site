from django.db import models

# Create your models here.
class Event(models.Model):
    title = models.CharField(max_length=100)
    date = models.DateField()
    start_time = models.TimeField()
    end_time = models.TimeField(null=True, blank=True)
    address = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    state = models.CharField(max_length=2)
    zip = models.IntegerField()
    description = models.TextField()
    actionnetwork_url = models.URLField()

    def __str__(self):
        return self.title + ' ' + str(self.date)


