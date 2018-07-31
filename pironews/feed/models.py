from django.db import models
from django.utils import timezone


class Republicdb(models.Model):
    title = models.CharField(max_length=600)
    href = models.CharField(max_length=600, default="2")

    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering=["-created_date"]




class Indiatvdb(models.Model):
    title = models.CharField(max_length=600)
    href = models.CharField(max_length=600,default="2")
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering=["-created_date"]


class NDTVdb(models.Model):
    title = models.CharField(max_length=600)
    href = models.CharField(max_length=600, default="2")
    created_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title

    class Meta:
        ordering=["-created_date"]
