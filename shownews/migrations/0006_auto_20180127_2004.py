# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-27 12:04
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shownews', '0005_scrapingrule_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='scrapingrule',
            name='name',
            field=models.CharField(default='', max_length=100, unique=True),
        ),
    ]
