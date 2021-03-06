# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-09-13 19:04
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion
import magic.core.models.magic_models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='_image',
            field=models.FileField(blank=True, null=True, upload_to=magic.core.models.magic_models.card_image_path),
        ),
        migrations.AddField(
            model_name='deck',
            name='set',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='core.Set'),
        ),
        migrations.AlterField(
            model_name='deck',
            name='name',
            field=models.CharField(max_length=64, unique=True),
        ),
    ]
