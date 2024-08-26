from django.db import models
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