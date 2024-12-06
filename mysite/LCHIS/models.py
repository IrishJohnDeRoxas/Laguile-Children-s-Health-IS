from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.hashers import make_password
from django.utils import timezone
from django.contrib.auth.base_user import BaseUserManager
from django.core.files.storage import default_storage
from .validators import validate_today_date
from django.core.exceptions import ValidationError
from django.core.validators import MinLengthValidator, MaxLengthValidator
from datetime import datetime
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
    
    mother_first_name = models.CharField(max_length=200, blank=False)
    mother_middle_name = models.CharField(max_length=200, blank=False)
    mother_last_name = models.CharField(max_length=200, blank=False)
    
    father_first_name = models.CharField(max_length=200, blank=False)
    father_middle_name = models.CharField(max_length=200, blank=False)
    father_last_name = models.CharField(max_length=200, blank=False)
    
    bcg = models.CharField(max_length=200, null=True, blank=True, validators=[validate_today_date])
    hepa_b = models.CharField(max_length=200, null=True, blank=True, validators=[validate_today_date])
    penta_1 = models.CharField(max_length=200, null=True, blank=True, validators=[validate_today_date])
    penta_2 = models.CharField(max_length=200, null=True, blank=True, validators=[validate_today_date])
    penta_3 = models.CharField(max_length=200, null=True, blank=True, validators=[validate_today_date])
    opv_1 = models.CharField(max_length=200, null=True, blank=True, validators=[validate_today_date])
    opv_2 = models.CharField(max_length=200, null=True, blank=True, validators=[validate_today_date])
    opv_3 = models.CharField(max_length=200, null=True, blank=True, validators=[validate_today_date])
    ipv_1 = models.CharField(max_length=200, null=True, blank=True, validators=[validate_today_date])
    ipv_2 = models.CharField(max_length=200, null=True, blank=True, validators=[validate_today_date])
    pcv_1 = models.CharField(max_length=200, null=True, blank=True, validators=[validate_today_date])
    pcv_2 = models.CharField(max_length=200, null=True, blank=True, validators=[validate_today_date])
    pcv_3 = models.CharField(max_length=200, null=True, blank=True, validators=[validate_today_date])
    mcv_1 = models.CharField(max_length=200, null=True, blank=True, validators=[validate_today_date])
    mcv_2 = models.CharField(max_length=200, null=True, blank=True, validators=[validate_today_date])
    
    remarks = models.CharField(max_length=200, blank=False)
    
    
    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
    def delete(self, *args, **kwargs):
        if self.image:
            self.image.delete(save=False)
        super().delete(*args, **kwargs)
       
    def clean(self):
        field_names = [
                    'bcg',
                    'hepa_b',
                    'penta_1',
                    'penta_2',
                    'penta_3',
                    'opv_1',
                    'opv_2',
                    'opv_3',
                    'ipv_1',
                    'ipv_2',
                    'pcv_1',
                    'pcv_2',
                    'pcv_3',
                    'mcv_1',
                    'mcv_2'
                    ]
        
        b_day = datetime.strptime(self.birthdate, '%B %d, %Y').date()

        errors = {}
        for field_name in field_names:
            field_value = getattr(self, field_name)
            if field_value:
                try:
                    field_date = datetime.strptime(field_value, '%B %d, %Y').date()
                    if b_day > field_date:
                        errors[field_name] = f"{field_name} should be older than the child's birthdate."
                except ValueError:
                    errors[field_name] = f"Invalid date format for {field_name}. Please use the format 'Month Day, Year'."

        if errors:
            raise ValidationError(errors)

        return super().clean() 
    
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

    if len(password) < 4:
      raise ValueError('Password must be at least 4 characters long.')

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
  password = models.CharField(max_length=128, validators=[
        MinLengthValidator(4),
        MaxLengthValidator(10),
    ], error_messages={
        'min_length': 'Password must be at least 4 characters long.',
        'max_length': 'Password cannot exceed 10 characters.'
    })

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