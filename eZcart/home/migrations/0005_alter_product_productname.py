# Generated by Django 5.1.4 on 2025-02-07 05:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('home', '0004_alter_product_productprice'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='productName',
            field=models.CharField(max_length=100),
        ),
    ]
