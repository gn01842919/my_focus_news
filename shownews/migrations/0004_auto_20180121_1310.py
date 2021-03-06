# -*- coding: utf-8 -*-
# Generated by Django 1.11.9 on 2018-01-21 05:10
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shownews', '0003_auto_20180119_2059'),
    ]

    operations = [
        migrations.CreateModel(
            name='NewsCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True)),
            ],
        ),
        migrations.AddField(
            model_name='newsdata',
            name='rules',
            field=models.ManyToManyField(to='shownews.ScrapingRule'),
        ),
        migrations.AddField(
            model_name='scrapingrule',
            name='tags',
            field=models.ManyToManyField(to='shownews.NewsCategory'),
        ),
    ]
