# Generated by Django 5.1 on 2024-09-29 11:12

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('LCHIS', '0037_remove_guardianmodel_middle_name_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='guardianmodel',
            name='date_joined',
            field=models.DateField(default=django.utils.timezone.now),
        ),
    ]
