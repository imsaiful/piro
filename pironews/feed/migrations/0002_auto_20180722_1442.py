# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-22 09:12
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='headline',
            name='image',
            field=models.FileField(default='image of post', upload_to=''),
        ),
        migrations.AlterField(
            model_name='headline',
            name='title',
            field=models.CharField(max_length=600),
        ),
    ]