from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _
from apps.accounts.models import *
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import ValidationError


def validate_time(value):
    if value % 2 != 0 or value < 0 or value > 22:
        raise ValidationError(
            _('%(value)s is not valid'),
            params={'value': value},
        )


class Schedule(models.Model):
    DAY_CHOICES = (
        (0, 'Saturday'),
        (1, 'Sunday'),
        (2, 'Monday'),
        (3, 'Tuesday'),
        (4, 'Wednesday'),
        (5, 'Thursday'),
        (6, 'Friday')
    )
    day = models.IntegerField(choices=DAY_CHOICES, verbose_name=_('days in week'))

    time = models.IntegerField(validators=[validate_time], verbose_name=_('times in day'))

    def as_json(self):
        return dict(day=self.day, time=self.time)


class Project(models.Model):
    organization = models.ForeignKey(OrganizationProfile)
    STATUS_CHOICES = (
        ('not_started', 'not_started'),
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

    def as_json(self):
        benefactors_list = []
        for ben in self.benefactors.all():
            benefactors_list.append(ben.as_json())

        return dict(organization=self.organization.as_json(), name=self.name, status=self.status,
                    id=self.id, benefactors=benefactors_list,
                    money_needed=self.money_needed, money_donated=self.money_donated)


class NonFinancialProject(Project):
    benefactor = models.ForeignKey(BenefactorProfile, null=True)
    need = models.ForeignKey(BenefactorSkill, null=False)
    GENDER_CHOICES = (
        ('مرد', 'مرد'),
        ('زن', 'زن'),
        ('اهمیتی ندارد', 'اهمیتی‌ ندارد'),
    )
    gender = models.CharField(max_length=20, choices=GENDER_CHOICES, default='N', verbose_name=_('gender‌'))
    age = models.IntegerField(null=True, blank=True, verbose_name=_('Age‌'))
    location = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('location'))
    schedule = models.ManyToManyField(Schedule)

    def get_schedule_list(self):
        schedule_list = []
        for schedule in self.schedule.all():
            schedule_list.append(schedule.as_json())

    def as_json(self):
        return dict(organization=self.organization.as_json(), name=self.name, status=self.status,
                    id=self.id, benefactor=self.benefactor.as_json(), schedule=self.get_schedule_list(),
                    need_=dict(name=self.need.name, category=self.need.category),
                    gender=self.gender, age=self.age, location=self.location)


class Feedback(models.Model):
    FEEDER_CHOICES = (
        ('benefactor', 'benefactor'),
        ('organization', 'organization'),
    )
    feeder = models.CharField(max_length=20, choices=FEEDER_CHOICES, default='organization', verbose_name=_('feeder‌'))
    project = models.ForeignKey(NonFinancialProject)

    rate = models.IntegerField(default=5, validators=[MaxValueValidator(5), MinValueValidator(1)])

    feedback = models.CharField(max_length=1000, null=True, blank=True, verbose_name=_('feedback'))

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
