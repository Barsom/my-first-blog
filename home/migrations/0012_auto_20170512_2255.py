# -*- coding: utf-8 -*-
# Generated by Django 1.11 on 2017-05-12 20:55
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import home.views


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0011_auto_20170512_2248'),
    ]

    operations = [
        migrations.AlterField(
            model_name='grade',
            name='subject1final',
            field=models.PositiveIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MaxValueValidator(100), home.views.validate_nonzero], verbose_name='Subject 1 Final'),
        ),
        migrations.AlterField(
            model_name='grade',
            name='subject1mid',
            field=models.PositiveIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MaxValueValidator(100), home.views.validate_nonzero], verbose_name='Subject 1 Midterm'),
        ),
        migrations.AlterField(
            model_name='grade',
            name='subject1practical',
            field=models.PositiveIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MaxValueValidator(100), home.views.validate_nonzero], verbose_name='Subject 1 Practical'),
        ),
        migrations.AlterField(
            model_name='grade',
            name='subject2final',
            field=models.PositiveIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MaxValueValidator(100), home.views.validate_nonzero], verbose_name='Subject 2 Final'),
        ),
        migrations.AlterField(
            model_name='grade',
            name='subject2mid',
            field=models.PositiveIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MaxValueValidator(100), home.views.validate_nonzero], verbose_name='Subject 2 Midterm'),
        ),
        migrations.AlterField(
            model_name='grade',
            name='subject2practical',
            field=models.PositiveIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MaxValueValidator(100), home.views.validate_nonzero], verbose_name='Subject 2 Practical'),
        ),
        migrations.AlterField(
            model_name='grade',
            name='subject3final',
            field=models.PositiveIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MaxValueValidator(100), home.views.validate_nonzero], verbose_name='Subject 3 Final'),
        ),
        migrations.AlterField(
            model_name='grade',
            name='subject3mid',
            field=models.PositiveIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MaxValueValidator(100), home.views.validate_nonzero], verbose_name='Subject 3 Midterm'),
        ),
        migrations.AlterField(
            model_name='grade',
            name='subject3practical',
            field=models.PositiveIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MaxValueValidator(100), home.views.validate_nonzero], verbose_name='Subject 3 Practical'),
        ),
        migrations.AlterField(
            model_name='grade',
            name='subject4final',
            field=models.PositiveIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MaxValueValidator(100), home.views.validate_nonzero], verbose_name='Subject 4 Final'),
        ),
        migrations.AlterField(
            model_name='grade',
            name='subject4mid',
            field=models.PositiveIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MaxValueValidator(100), home.views.validate_nonzero], verbose_name='Subject 4 Midterm'),
        ),
        migrations.AlterField(
            model_name='grade',
            name='subject4practical',
            field=models.PositiveIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MaxValueValidator(100), home.views.validate_nonzero], verbose_name='Subject 4 Practical'),
        ),
        migrations.AlterField(
            model_name='grade',
            name='subject5final',
            field=models.PositiveIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MaxValueValidator(100), home.views.validate_nonzero], verbose_name='Subject 5 Final'),
        ),
        migrations.AlterField(
            model_name='grade',
            name='subject5mid',
            field=models.PositiveIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MaxValueValidator(100), home.views.validate_nonzero], verbose_name='Subject 5 Midterm'),
        ),
        migrations.AlterField(
            model_name='grade',
            name='subject5practical',
            field=models.PositiveIntegerField(blank=True, default=None, null=True, validators=[django.core.validators.MaxValueValidator(100), home.views.validate_nonzero], verbose_name='Subject 5 Practical'),
        ),
    ]
