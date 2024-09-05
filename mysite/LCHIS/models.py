from django.db import models
import os
# Create your models here.

class ChildModel(models.Model):
    first_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    image_path = models.TextField(null=True)
    years_old = models.PositiveIntegerField(null=True)
    months_old = models.PositiveIntegerField(null=True)
    gender = models.CharField(max_length=1)
    
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

# TODO add gallery model
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