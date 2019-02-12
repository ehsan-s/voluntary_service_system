from django.db import models
from datetime import datetime


class Log(models.Model):
    message = models.CharField(null=False, blank=False, max_length=200)
    time = models.DateTimeField(default=datetime.now, blank=False)
