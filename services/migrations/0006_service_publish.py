# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-16 10:46
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0005_auto_20170616_1039'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='publish',
            field=models.BooleanField(default=False, verbose_name='Julkinen'),
        ),
    ]
