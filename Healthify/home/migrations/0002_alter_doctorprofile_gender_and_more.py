# Generated by Django 5.1.4 on 2025-04-09 13:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='doctorprofile',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='doctorprofile',
            name='specialization',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AlterField(
            model_name='patientprofile',
            name='age',
            field=models.PositiveIntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='patientprofile',
            name='gender',
            field=models.CharField(choices=[('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')], max_length=10, null=True),
        ),
        migrations.AlterField(
            model_name='patientprofile',
            name='phone',
            field=models.CharField(max_length=15, null=True, unique=True),
        ),
    ]
