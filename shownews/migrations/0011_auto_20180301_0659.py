# -*- coding: utf-8 -*-
# Generated by Django 1.11.10 on 2018-03-01 06:59
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shownews', '0010_auto_20180228_0757'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newsdata',
            name='url',
            field=models.URLField(max_length=500, unique=True),
        ),
    ]
