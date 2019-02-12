from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _


class SkillCategory(models.Model):
    category = models.CharField(max_length=100, null=False, blank=False, unique=True, verbose_name=_('skill category‌'))


class BenefactorSkill(models.Model):
    category = models.ForeignKey(SkillCategory)
    name = models.CharField(max_length=100, null=False, blank=False, unique=True, verbose_name=_('skill name‌'))

    def as_json(self):
        return dict(category=self.category.category, name=self.name)


# a_cat = SkillCategory(category='معلم')
# a_cat.save()
# a_skl = BenefactorSkill(category=a_cat, name='فیزیک')


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='user_profile')
    phone_number = models.CharField(max_length=20, null=False, blank=False, verbose_name=_('Mobile number‌'))
    tel_number = models.CharField(max_length=20, null=False, blank=False, verbose_name=_('Telephone number‌'))
    address = models.CharField(max_length=200, null=False, blank=False, verbose_name=_('Address‌'))
    activities = models.CharField(max_length=1000, null=True, blank=True, verbose_name=_('Activities‌'))
    city = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('location'))

    STATUS_CHOICES = (
        ('P', 'pending'),
        ('V', 'verified'),
    )
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, default='V', verbose_name=_('User status'))


class OrganizationProfile(models.Model):
    profile = models.OneToOneField(UserProfile)
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('Name‌'))

    def as_json(self):
        return dict(username=self.profile.user.username,
                    email=self.profile.user.email,
                    phone_number=self.profile.phone_number, tel_number=self.profile.tel_number,
                    address=self.profile.address, city=self.profile.city,
                    activities=self.profile.activities,
                    name=self.name)


class BenefactorProfile(models.Model):
    profile = models.OneToOneField(UserProfile)
    age = models.IntegerField(null=False, blank=False, verbose_name=_('Age‌'))
    desires = models.CharField(max_length=1000, null=True, blank=True, verbose_name=_('Desires'))
    skills = models.ManyToManyField(BenefactorSkill)
    GENDER_CHOICES = (
        ('M', 'مرد'),
        ('F', 'زن'),
        ('N', 'اهمیتی‌ ندارد'),
    )
    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, default='N', verbose_name=_('gender‌'))

    def as_json(self):
        return dict(username=self.profile.user.username,
                    first_name=self.profile.user.first_name,
                    last_name=self.profile.user.last_name,
                    email=self.profile.user.email,
                    gender=self.gender,
                    city=self.profile.city,
                    phone_number=self.profile.phone_number, tel_number=self.profile.tel_number,
                    address=self.profile.address, activities=self.profile.activities,
                    age=self.age, desires=self.desires, skills=self.get_all_skills())

    def get_all_skills(self):
        all_skills = []
        for skill in self.skills.all():
            all_skills.append(dict(category=skill.category.category, name=skill.name))
        return all_skills
