# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-17 17:42
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wordcount', '0002_auto_20170617_1726'),
    ]

    operations = [
        migrations.AlterField(
            model_name='word',
            name='count',
            field=models.BigIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='word',
            name='word',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]
