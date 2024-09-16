from django.db import models
import os
# Create your models here.

# TODO Add Blank False on the required fields
class ChildModel(models.Model):
    genderChoices = (
        ('M', 'Male'),
        ('F', 'Female'),
    )
    
    barangay = models.CharField(max_length=200,default='Laguile')
    name_of_bhw = models.CharField(max_length=200)
    purok = models.CharField(max_length=200)
    nurse = models.CharField(max_length=200)
    
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    image = models.ImageField(null=True, upload_to='child/', blank=True)
    birthdate = models.CharField(max_length=200)
    years_old = models.PositiveIntegerField(null=True, blank=True)
    months_old = models.PositiveIntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=genderChoices, default='M')
    
    bcg = models.CharField(max_length=200, null=True)
    hepa_b = models.CharField(max_length=200, null=True)
    penta_1 = models.CharField(max_length=200, null=True)
    penta_2 = models.CharField(max_length=200, null=True)
    penta_3 = models.CharField(max_length=200, null=True)
    opv_1 = models.CharField(max_length=200, null=True)
    opv_2 = models.CharField(max_length=200, null=True)
    opv_3 = models.CharField(max_length=200, null=True)
    ipv_1 = models.CharField(max_length=200, null=True)
    ipv_2 = models.CharField(max_length=200, null=True)
    pcv_1 = models.CharField(max_length=200, null=True)
    pcv_2 = models.CharField(max_length=200, null=True)
    pcv_3 = models.CharField(max_length=200, null=True)
    mcv_1 = models.CharField(max_length=200, null=True)
    mcv_2 = models.CharField(max_length=200, null=True)
    
    remarks = models.CharField(max_length=200, null=True)

    
class GuardianModel(models.Model):
    children = models.ManyToManyField(ChildModel)
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    username = models.CharField(max_length=200,null=True)
    password = models.CharField(max_length=200, null=True)
    
    
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