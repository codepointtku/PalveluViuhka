# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2019-04-02 12:26
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0023_auto_20180903_2046'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='labour_hire',
            field=models.BooleanField(default=False, verbose_name='Vuokratyo'),
        ),
    ]
