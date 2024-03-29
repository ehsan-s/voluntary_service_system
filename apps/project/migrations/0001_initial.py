# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-02-13 07:16
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Feedback',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('feeder', models.CharField(choices=[('benefactor', 'benefactor'), ('organization', 'organization')], default='organization', max_length=20, verbose_name='feeder\u200c')),
                ('rate', models.IntegerField(default=5, validators=[django.core.validators.MaxValueValidator(5), django.core.validators.MinValueValidator(1)])),
                ('feedback', models.CharField(blank=True, max_length=1000, null=True, verbose_name='feedback')),
            ],
        ),
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('not_started', 'not_started'), ('in_progress', 'in progress'), ('done', 'done')], default='not_started', max_length=20, verbose_name='status\u200c')),
                ('name', models.CharField(max_length=100, verbose_name='project name\u200c')),
            ],
        ),
        migrations.CreateModel(
            name='Request',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('requester', models.CharField(choices=[('benefactor', 'benefactor'), ('organization', 'organization')], default='benefactor', max_length=20, verbose_name='requester\u200c')),
                ('request_desc', models.CharField(blank=True, max_length=1000, null=True, verbose_name='request description\u200c')),
                ('answer_desc', models.CharField(blank=True, max_length=1000, null=True, verbose_name='answer description\u200c')),
                ('status', models.CharField(choices=[('in_progress', 'in_progress'), ('accepted', 'accepted'), ('rejected', 'rejected')], default='in_progress', max_length=20, verbose_name='status\u200c')),
                ('benefactor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.BenefactorProfile')),
            ],
        ),
        migrations.CreateModel(
            name='FinancialProject',
            fields=[
                ('project_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='project.Project')),
                ('deadline', models.DateTimeField(blank=True, null=True)),
                ('money_needed', models.IntegerField(verbose_name='money needed\u200c')),
                ('money_donated', models.IntegerField(null=True, verbose_name='money donated\u200c')),
                ('benefactors', models.ManyToManyField(to='accounts.BenefactorProfile')),
            ],
            bases=('project.project',),
        ),
        migrations.CreateModel(
            name='NonFinancialProject',
            fields=[
                ('project_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='project.Project')),
                ('gender', models.CharField(choices=[('مرد', 'مرد'), ('زن', 'زن'), ('اهمیتی ندارد', 'اهمیتی\u200c ندارد')], default='اهمیتی ندارد', max_length=20, verbose_name='gender\u200c')),
                ('age', models.IntegerField(blank=True, null=True, verbose_name='Age\u200c')),
                ('location', models.CharField(max_length=100, verbose_name='location')),
                ('benefactor', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.BenefactorProfile')),
                ('need', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.BenefactorSkill')),
                ('schedule', models.ManyToManyField(to='accounts.Schedule')),
            ],
            bases=('project.project',),
        ),
        migrations.AddField(
            model_name='project',
            name='organization',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.OrganizationProfile'),
        ),
        migrations.AddField(
            model_name='request',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.NonFinancialProject'),
        ),
        migrations.AddField(
            model_name='feedback',
            name='project',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='project.NonFinancialProject'),
        ),
    ]
