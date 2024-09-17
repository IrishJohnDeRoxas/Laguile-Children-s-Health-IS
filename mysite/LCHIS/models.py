from django.db import models
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
    
    first_name = models.CharField(max_length=200, blank=False)
    middle_name = models.CharField(max_length=200, blank=False)
    last_name = models.CharField(max_length=200, blank=False)
    image = models.ImageField(null=True, upload_to='child/', blank=True)
    birthdate = models.CharField(max_length=200)
    years_old = models.PositiveIntegerField(null=True, blank=True)
    months_old = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=genderChoices, default='M')
    
    bcg = models.CharField(max_length=200)
    hepa_b = models.CharField(max_length=200)
    penta_1 = models.CharField(max_length=200)
    penta_2 = models.CharField(max_length=200)
    penta_3 = models.CharField(max_length=200)
    opv_1 = models.CharField(max_length=200)
    opv_2 = models.CharField(max_length=200)
    opv_3 = models.CharField(max_length=200)
    ipv_1 = models.CharField(max_length=200)
    ipv_2 = models.CharField(max_length=200)
    pcv_1 = models.CharField(max_length=200)
    pcv_2 = models.CharField(max_length=200)
    pcv_3 = models.CharField(max_length=200)
    mcv_1 = models.CharField(max_length=200)
    mcv_2 = models.CharField(max_length=200)
    
    remarks = models.CharField(max_length=200, blank=False)

    
class GuardianModel(models.Model):
    children = models.ManyToManyField(ChildModel)
    first_name = models.CharField(max_length=200, blank=False)
    middle_name = models.CharField(max_length=200, blank=False)
    last_name = models.CharField(max_length=200, blank=False)
    username = models.CharField(max_length=200, blank=False)
    password = models.CharField(max_length=200, blank=False)
    
    
# class GivenVaccine(models.Model):
#     child = models.ForeignKey(Child, on_delete=models.CASCADE)
#     date_given = models.DateTimeField("date published")
#     name = models.TextField(null=True)
#     description = models.TextField(null=True)
    
# class Vaccine(models.Model):
#     given_vaccine = models.ForeignKey(GivenVaccine, on_delete=models.CASCADE)
#     name = models.TextField(null=True)
#     description = models.TextField(null=True)

# class AboutUs(models.Model):
#     header = models.TextField(null=True)
#     description = models.TextField(null=True)

class GalleryModel(models.Model):
    typeChoices = (
        ('health-center', 'Health Center'),
        ('barangay-hall', 'Barangay Hall'),
        ('school', 'School'),
        ('basketball-court', 'Basketball Court'),
        ('church', 'Church'),
        ('other', 'Other'),
    )

    image = models.ImageField(null=True, upload_to='gallery/')
    type = models.CharField(null=True, max_length=200, choices=typeChoices)
    date = models.TextField()

    def delete(self, *args, **kwargs):
        if self.image:
            if os.path.isfile(self.image.path):
                os.remove(self.image.path)
        super().delete(*args, **kwargs)