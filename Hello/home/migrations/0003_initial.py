# Generated by Django 5.1.4 on 2025-01-02 03:34

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('home', '0002_delete_customers'),
    ]

    operations = [
        migrations.CreateModel(
            name='Customer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Username', models.CharField(max_length=20)),
                ('email', models.CharField(max_length=30)),
                ('gender', models.CharField(max_length=10)),
                ('age', models.IntegerField()),
                ('phone', models.CharField(max_length=15)),
            ],
        ),
    ]
