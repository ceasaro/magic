# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-17 15:12
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20170913_1904'),
    ]

    operations = [
        migrations.RenameField(
            model_name='card',
            old_name='_image',
            new_name='image',
        ),
    ]
