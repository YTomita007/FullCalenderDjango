from django.db import models

class Event(models.Model):
    id = models.IntegerField(primary_key=True)
    start_date = models.DateField()
    end_date = models.DateField()
    event_name = models.CharField(max_length=200)