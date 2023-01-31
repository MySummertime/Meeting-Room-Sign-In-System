
from django.db import models
from signSystem.models.event import Event

# Create your models here.

class Guest(models.Model):
    '''Guest db table'''
    event = models.ForeignKey(Event, on_delete=models.CASCADE)  # associate with Event ID
    realname = models.CharField(max_length=128)
    phone = models.CharField(max_length=16)
    email = models.EmailField()
    sign = models.BooleanField()
    create_time = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('event', 'phone')
        ordering = ['-id']

    def __str__(self) -> str:
        return self.realname