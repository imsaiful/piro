# -*- coding: utf-8 -*-
# Generated by Django 1.11.14 on 2018-07-31 16:16
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('feed', '0008_auto_20180731_1328'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='indiatvdb',
            options={'ordering': ['-created_date']},
        ),
        migrations.AlterModelOptions(
            name='ndtvdb',
            options={'ordering': ['-created_date']},
        ),
        migrations.AlterModelOptions(
            name='republicdb',
            options={'ordering': ['-created_date']},
        ),
    ]