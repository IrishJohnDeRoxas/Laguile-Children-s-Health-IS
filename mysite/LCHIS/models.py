from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.core.files.storage import default_storage

import os
# Create your models here.

class ChildModel(models.Model):
    genderChoices = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    
    barangay = models.CharField(max_length=200, default='Laguile')
    name_of_bhw = models.CharField(max_length=200, blank=False)
    purok = models.CharField(max_length=200, blank=False)
    nurse = models.CharField(max_length=200, blank=False)
    
    child_first_name = models.CharField(max_length=200, blank=False)
    child_middle_name = models.CharField(max_length=200, blank=False)
    child_last_name = models.CharField(max_length=200, blank=False)
    image = models.ImageField(null=True, upload_to='child/', blank=True)
    
    height = models.CharField(max_length=200, blank=False)
    weight = models.CharField(max_length=200, blank=False)
    condition = models.TextField(blank=False)
    birthdate = models.CharField(max_length=200)
    years_old = models.PositiveIntegerField(null=True, blank=True)
    months_old = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=genderChoices, default='M')
    
    name_of_mother = models.CharField(max_length=200, blank=True)
    mother_history = models.TextField(blank=True)
    name_of_father = models.CharField(max_length=200, blank=True)
    father_history = models.TextField(blank=True)
    
    bcg = models.CharField(max_length=200, null=True, blank=True)
    hepa_b = models.CharField(max_length=200, null=True, blank=True)
    penta_1 = models.CharField(max_length=200, null=True, blank=True)
    penta_2 = models.CharField(max_length=200, null=True, blank=True)
    penta_3 = models.CharField(max_length=200, null=True, blank=True)
    opv_1 = models.CharField(max_length=200, null=True, blank=True)
    opv_2 = models.CharField(max_length=200, null=True, blank=True)
    opv_3 = models.CharField(max_length=200, null=True, blank=True)
    ipv_1 = models.CharField(max_length=200, null=True, blank=True)
    ipv_2 = models.CharField(max_length=200, null=True, blank=True)
    pcv_1 = models.CharField(max_length=200, null=True, blank=True)
    pcv_2 = models.CharField(max_length=200, null=True, blank=True)
    pcv_3 = models.CharField(max_length=200, null=True, blank=True)
    mcv_1 = models.CharField(max_length=200, null=True, blank=True)
    mcv_2 = models.CharField(max_length=200, null=True, blank=True)
    
    remarks = models.CharField(max_length=200, blank=False)
    
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete(save=False)
        super().delete(*args, **kwargs)
        
    def save(self, *args, **kwargs):
        if self.pk:  # Check if the instance is being updated
            try:
                old_image = ChildModel.objects.get(pk=self.pk).image
            except ChildModel.DoesNotExist:
                old_image = None

            if old_image and self.image != old_image:
                default_storage.delete(old_image.name)

        super().save(*args, **kwargs)
        
    def delete_image(self):
        if self.image:
            default_storage.delete(self.image.name)
            self.image = None
            self.save()

class GuardianManager(BaseUserManager):
    def create_user(self, username, password, **extra_fields):
        # Customize user creation logic (e.g., email validation)
        if not username:
            raise ValueError('The username field is required')
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password, **extra_fields):
        # Customize superuser creation logic (e.g., grant all permissions)
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')

        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(username, password, **extra_fields)
    
class GuardianModel(AbstractUser):
    objects = GuardianManager()
    child = models.ForeignKey(ChildModel, on_delete=models.CASCADE, null=True, blank=True)
    date_joined = models.DateField(default=timezone.now, null=True, blank=True)
    middle_name = models.CharField(max_length=200, blank=False)

class GalleryModel(models.Model):
    typeChoices = (
        ('health-center', 'Health Center'),
        ('program', 'Program'),
    )

    image = models.ImageField(null=True, upload_to='gallery/')
    type = models.CharField(null=True, max_length=200, choices=typeChoices)
    date = models.TextField()

    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)
        
class VitaminModel(models.Model):
    image = models.ImageField(null=True, upload_to='vitamins/')
    name = models.CharField(max_length=200, blank=False)
    description = models.TextField()
    quantity = models.IntegerField(default=0)

    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)
        
class AboutUsModel(models.Model):
    header = models.CharField(max_length=200, blank=False)
    description = models.TextField()
    on_left = models.BooleanField(default=False)
    
class ContactUsModel(models.Model):
    typeChoices = (
        ('address', 'Address'),
        ('contact_number', 'Contact Number'),
        ('email', 'Email'),
    )
    contact_type = models.CharField(max_length=200, blank=False, choices=typeChoices, default='address')
    header = models.CharField(max_length=200, blank=False)
    description = models.TextField()