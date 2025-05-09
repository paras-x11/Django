# Generated by Django 5.2 on 2025-04-10 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0002_alter_doctorprofile_gender_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='doctorprofile',
            name='doctor_image',
            field=models.ImageField(null=True, upload_to='doctor_images'),
        ),
        migrations.AddField(
            model_name='patientprofile',
            name='patient_image',
            field=models.ImageField(null=True, upload_to='patient_images'),
        ),
    ]
