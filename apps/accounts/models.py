from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    phone_number = models.CharField(max_length=20, null=False, blank=False, verbose_name=_('Mobile number‌'))
    tel_number = models.CharField(max_length=20, null=False, blank=False, verbose_name=_('Telephone number‌'))
    address = models.CharField(max_length=200, null=False, blank=False, verbose_name=_('Address‌'))
    activities = models.CharField(max_length=1000, null=True, blank=True, verbose_name=_('Activities‌'))


class OrganizationProfile(models.Model):
    profile = models.OneToOneField(UserProfile)
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('Name‌'))


class BenefactorProfile(models.Model):
    profile = models.OneToOneField(UserProfile)
    age = models.IntegerField(null=False, blank=False, verbose_name=_('Age‌'))
    desires = models.CharField(max_length=1000, null=True, blank=True, verbose_name=_('Desires'))
    skills = models.ManyToManyField(BenefactorSkill)


class SkillCategory(models.Model):
    category = models.CharField(max_length=100, null=False, blank=False, unique=True, verbose_name=_('skill category‌'))


class BenefactorSkill(models.Model):
    category = models.ForeignKey(SkillCategory)
    name = models.CharField(max_length=100, null=False, blank=False, unique=True, verbose_name=_('skill name‌'))