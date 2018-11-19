from django.db import models
from django.utils import timezone


# Create your models here.
class Republic(models.Model):
    headline = models.TextField(null=False)
    link = models.TextField(null=False)
    date = models.DateTimeField(default=timezone.now)
    category = models.TextField(null=True)
    sentiment = models.TextField(null=True)

    def __str__(self):
        return self.headline

    class Meta:
        ordering = ["-id"]


class Indiatoday(models.Model):
    headline = models.TextField(null=False)
    link = models.TextField(null=False)
    date = models.DateTimeField(default=timezone.now)
    category = models.TextField(null=True)
    sentiment = models.TextField(null=True)

    def __str__(self):
        return self.headline

    class Meta:
        ordering = ["-id"]


class Ndtv(models.Model):
    headline = models.TextField(null=False)
    link = models.TextField(null=False)
    date = models.DateTimeField(default=timezone.now)
    category = models.TextField(null=True)
    sentiment = models.TextField(null=True)

    def __str__(self):
        context={
            "headline":self.headline,
            "category":self.category
        }
        return context

    class Meta:
        ordering = ["-id"]



class Hindustan(models.Model):
    headline = models.TextField(null=False)
    link = models.TextField(null=False)
    date = models.DateTimeField(default=timezone.now)
    category = models.TextField(null=True)
    sentiment = models.TextField(null=True)

    def __str__(self):
        context={
            "headline":self.headline,
            "category":self.category
        }
        return context

    class Meta:
        ordering = ["-id"]