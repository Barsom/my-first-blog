# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-12 14:07
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_remove_lecture_subject'),
    ]

    operations = [
        migrations.AddField(
            model_name='lecture',
            name='subject',
            field=models.CharField(blank=True, default=None, max_length=50, null=True),
        ),
    ]
