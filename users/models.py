from django.db import models
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.contrib.auth.models import User

GENDER_CHOICES = [
    ('Male', 'Male'),
    ('Female', 'Female')
]

STATUS_CHOICES = [
    ('Married', 'Married'),
    ('Single', 'Single')
]

PROFESSION_CHOICES = [
    ('Student or Learning', 'Student or Learning'),
    ('Junior Developer', 'Junior Developer'),
    ('Middle Developer', 'Middle Developer'),
    ('Senior Developer', 'Senior Developer'),
    ('Developer', 'Developer'),
    ('Manager', 'Manager'),
    ('Instructor or Teacher', 'Instructor or Teacher'),
    ('Intern', 'Intern'),
    ('Digital Marketer', 'Digital Marketer'),
    ('Data Scientist', 'Data Scientist'),
]

DEGREE_CHOICES = [
    ('IT', 'Information Technologies'),
    ('Bussiness Managment', 'Bussiness Managment'),
    ('Digital Marketing', 'Digital Marketing'),
    ('Computer Science', 'Computer Science'),
    ('Civil Engineering', 'Civil Engineering'),
    ('AI', 'Artificial & Inteligence'),
    ('Other', 'Other')
]


# PROFILE MODEL MANAGER
class ProfileManager(models.Manager):
    def get_auth_profile(self, profile, user, *args, **kwargs):
        return get_object_or_404(self, pk=profile, user=user)

    def check_auth_profile(self, user, *args, **kwargs):
        try:
            obj = self.get(user=user)
            if obj:
                return obj
        except Profile.DoesNotExist:
            return None


# PROFILE MODEL
class Profile(models.Model):
    user = models.OneToOneField(User, default=1, on_delete=models.CASCADE)
    name = models.CharField(max_length=80, default='username')
    age = models.IntegerField(default=0)
    gender = models.CharField(max_length=10, default=1, choices=GENDER_CHOICES)
    status = models.CharField(max_length=10, default=1, choices=STATUS_CHOICES)
    website = models.URLField(max_length=283, blank=True, null=True)
    company = models.CharField(max_length=120)
    profession = models.CharField(max_length=120, default='Web Developer', choices=PROFESSION_CHOICES)
    location = models.CharField(max_length=100, default='Bishkek')
    skills = models.CharField(max_length=120, choices=None, default='bomj')
    bio = models.TextField(blank=True, default='Hello pacany..!')
    image = models.ImageField(upload_to='profile_pics/', default='default.jpg', blank=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    objects = ProfileManager()

    def __str__(self, *args, **kwargs):
        return self.name

    def get_absolute_url(self, *args, **kwargs):
        return reverse('profiles:profiles-detail', kwargs={'id': self.pk})

    def get_update_url(self, *args, **kwargs):
        return reverse('profiles:profiles-update', kwargs={'id': self.pk})

    def get_delete_url(self, *args, **kwargs):
        return reverse('profiles:profiles-delete', kwargs={'id': self.pk})
