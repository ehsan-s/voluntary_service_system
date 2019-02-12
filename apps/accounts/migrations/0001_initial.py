# -*- coding: utf-8 -*-
# Generated by Django 1.11.17 on 2019-02-12 21:38
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BenefactorProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('age', models.IntegerField(verbose_name='Age\u200c')),
                ('desires', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Desires')),
                ('gender', models.CharField(choices=[('مرد', 'مرد'), ('زن', 'زن')], default='مرد', max_length=3, verbose_name='gender\u200c')),
            ],
        ),
        migrations.CreateModel(
            name='BenefactorSkill',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, unique=True, verbose_name='skill name\u200c')),
            ],
        ),
        migrations.CreateModel(
            name='OrganizationProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100, verbose_name='Name\u200c')),
            ],
        ),
        migrations.CreateModel(
            name='SkillCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('category', models.CharField(max_length=100, unique=True, verbose_name='skill category\u200c')),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phone_number', models.CharField(max_length=20, verbose_name='Mobile number\u200c')),
                ('tel_number', models.CharField(max_length=20, verbose_name='Telephone number\u200c')),
                ('address', models.CharField(max_length=200, verbose_name='Address\u200c')),
                ('activities', models.CharField(blank=True, max_length=1000, null=True, verbose_name='Activities\u200c')),
                ('city', models.CharField(default='Tehran', max_length=100, verbose_name='location')),
                ('status', models.CharField(choices=[('P', 'pending'), ('V', 'verified')], default='V', max_length=1, verbose_name='User status')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='user_profile', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='organizationprofile',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.UserProfile'),
        ),
        migrations.AddField(
            model_name='benefactorskill',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='accounts.SkillCategory'),
        ),
        migrations.AddField(
            model_name='benefactorprofile',
            name='profile',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='accounts.UserProfile'),
        ),
        migrations.AddField(
            model_name='benefactorprofile',
            name='skills',
            field=models.ManyToManyField(to='accounts.BenefactorSkill'),
        ),
    ]
