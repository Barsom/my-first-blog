# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-12 17:47
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0007_auto_20170512_1946'),
    ]

    operations = [
        migrations.CreateModel(
            name='Attendance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day1', models.NullBooleanField(verbose_name='Day 1')),
                ('day2', models.NullBooleanField(verbose_name='Day 2')),
                ('day3', models.NullBooleanField(verbose_name='Day 3')),
                ('day4', models.NullBooleanField(verbose_name='Day 4')),
                ('day5', models.NullBooleanField(verbose_name='Day 5')),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='home.Classroom')),
                ('student', models.OneToOneField(default=None, on_delete=django.db.models.deletion.CASCADE, to='home.Student')),
            ],
        ),
    ]
