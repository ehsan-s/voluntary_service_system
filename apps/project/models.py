from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from apps.accounts.models import *


class Project(models.Model):
    user = models.OneToOneField(User, related_name='user_profile')
    age = models.IntegerField(null=True, blank=True, verbose_name=_('Age‌'))
    phone_number = models.CharField(max_length=11, null=True, blank=True, verbose_name=_('Mobile number‌'))
    tel_number = models.CharField(max_length=20, null=True, blank=True, verbose_name=_('Telephone number‌'))
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Address‌'))
    activities = models.CharField(max_length=1000, null=True, blank=True, verbose_name=_('Activities‌'))


class FinancialProject(models.Model):
    organization = models.ForeignKey(OrganizationProfile)
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('financial project name‌'))
    deadline = models.DateTimeField(null=True, blank=True)


class NonFinancialProject(models.Model):
    need = models.ForeignKey(BenefactorSkill)
    GENDER_CHOICES = (
        ('MALE', 'male'),
        ('FEMALE', 'female'),
        ('NOT_IMPORTANT', 'not important'),
    )
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='NOT_IMPORTANT', verbose_name=_('gender‌'))
    city = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('city'))
    age = models.IntegerField(null=True, blank=True, verbose_name=_('Age‌'))