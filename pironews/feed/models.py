from django.db import models
from django.utils import timezone


class HeadLine(models.Model):
    title = models.CharField(max_length=600)
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title