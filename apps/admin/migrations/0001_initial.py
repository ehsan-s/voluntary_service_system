# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-02-13 07:16
from __future__ import unicode_literals

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Log',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('message', models.CharField(max_length=200)),
                ('time', models.DateTimeField(default=datetime.datetime.now)),
            ],
        ),
    ]
