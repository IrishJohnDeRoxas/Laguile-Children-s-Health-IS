# Generated by Django 5.1 on 2024-10-04 08:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LCHIS', '0041_alter_guardianmodel_managers'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gallerymodel',
            name='type',
            field=models.CharField(choices=[('health-center', 'Health Center'), ('program', 'Program')], max_length=200, null=True),
        ),
    ]
