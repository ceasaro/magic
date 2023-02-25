# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-04 10:58
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0004_auto_20171004_0731"),
    ]

    operations = [
        migrations.AddField(
            model_name="card",
            name="_supertypes",
            field=models.CharField(max_length=1024, null=True),
        ),
        migrations.AddField(
            model_name="card",
            name="cmc",
            field=models.IntegerField(default=0),
        ),
    ]
