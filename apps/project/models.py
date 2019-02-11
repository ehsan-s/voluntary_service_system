from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from apps.accounts.models import *
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType


class Project(models.Model):
    organization = models.ForeignKey(OrganizationProfile)
    STATUS_CHOICES = (
        ('not_started', 'not started'),
        ('in_progress', 'in progress'),
        ('done', 'done'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started', verbose_name=_('status‌'))
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('project name‌'))


class FinancialProject(Project):
    benefactors = models.ManyToManyField(BenefactorProfile)
    deadline = models.DateTimeField(null=True, blank=True)
    money_needed = models.IntegerField(null=False, verbose_name=_('money needed‌'))
    money_donated = models.IntegerField(null=True, verbose_name=_('money donated‌'))


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
    location = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('location'))


class Feedback(models.Model):
    FEEDER_CHOICES = (
        ('benefactor', 'benefactor'),
        ('organization', 'organization'),
    )
    feeder = models.CharField(max_length=20, choices=FEEDER_CHOICES, default='organization', verbose_name=_('feeder‌'))
    project = models.ForeignKey(NonFinancialProject)

    rate = models.IntegerField(default=5, validators=[MaxValueValidator(5), MinValueValidator(1)])

    feedback = models.CharField(max_length=1000, null=True, blank=True, verbose_name=_('feedback'))

    STATUS_CHOICES = (
        ('P', 'pending'),
        ('A', 'approved'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='P', verbose_name=_('User status'))

    def as_json(self):
        return dict(id=self.id, project=self.project, rate=self.rate, feedback=self.feedback)


class Request(models.Model):
    project = models.ForeignKey(NonFinancialProject)
    benefactor = models.ForeignKey(BenefactorProfile)

    REQUESTER_CHOICES = (
        ('benefactor', 'benefactor'),
        ('organization', 'organization'),
    )
    requester = models.CharField(max_length=20, choices=REQUESTER_CHOICES, default='benefactor', verbose_name=_('requester‌'))

    request_desc = models.CharField(max_length=1000, null=True, blank=True, verbose_name=_('request description‌'))
    answer_desc = models.CharField(max_length=1000, null=True, blank=True, verbose_name=_('answer description‌'))

    STATUS_CHOICES = (
        ('in_progress', 'in_progress'),
        ('accepted', 'accepted'),
        ('rejected', 'rejected'),
    )
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='in_progress', verbose_name=_('status‌'))
