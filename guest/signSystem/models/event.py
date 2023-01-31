
from django.db import models

# Create your models here.

class Event(models.Model):
    '''Event db table'''
    name = models.CharField(max_length=128)
    limit = models.IntegerField()
    status = models.BooleanField()
    address = models.CharField(max_length=256)
    start_time = models.DateTimeField(verbose_name='events time')
    create_time = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.name

