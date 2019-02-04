# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-02-04 20:10
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('project', '0003_auto_20190204_1447'),
    ]

    operations = [
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requester', models.CharField(choices=[('benefactor', 'benefactor'), ('organization', 'organization')], default='benefactor', max_length=20, verbose_name='requester\u200c')),
                ('request_desc', models.CharField(blank=True, max_length=1000, null=True, verbose_name='request description\u200c')),
                ('answer_desc', models.CharField(blank=True, max_length=1000, null=True, verbose_name='answer description\u200c')),
                ('status', models.CharField(choices=[('in_progress', 'in_progress'), ('accepted', 'accepted'), ('rejected', 'rejected')], default='in_progress', max_length=20, verbose_name='status\u200c')),
                ('benefactor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.BenefactorProfile')),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.NonFinancialProject')),
            ],
        ),
    ]
