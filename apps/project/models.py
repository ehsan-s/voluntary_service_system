from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from apps.accounts.models import *


class Project(models.Model):
    organization = models.ForeignKey(OrganizationProfile)
    STATUS_CHOICES = (
        ('in_progress', 'in progress'),
        ('done', 'done'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress', verbose_name=_('status‌'))
    location = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('location'))


class FinancialProject(Project):
    benefactors = models.ManyToManyField(BenefactorProfile)
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('financial project name‌'))
    deadline = models.DateTimeField(null=True, blank=True)
    money_needed = models.IntegerField(null=False, blank=False, verbose_name=_('money needed‌'))
    money_donated = models.IntegerField(null=False, blank=False, verbose_name=_('money donated‌'))


class NonFinancialProject(Project):
    benefactor = models.ForeignKey(BenefactorProfile, null=True)
    need = models.ForeignKey(BenefactorSkill, null=False)
    GENDER_CHOICES = (
        ('male', 'male'),
        ('female', 'female'),
        ('not_important', 'not important'),
    )
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='not_important', verbose_name=_('gender‌'))
    age = models.IntegerField(null=True, blank=True, verbose_name=_('Age‌'))


