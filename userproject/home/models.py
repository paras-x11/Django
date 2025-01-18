from django.db import models

# Create your models here.
class Customer(models.Model):
    username = models.CharField(max_length=20)
    email = models.CharField(max_length=20)
    age = models.IntegerField()
    gender = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    date_time = models.DateTimeField()

    def __str__(self):
        return self.username

class Contact(models.Model):
    name = models.CharField(max_length=20)
    email = models.EmailField(max_length=30)
    phone = models.CharField(max_length=15)
    desc = models.TextField(max_length=150)
    date_time = models.DateTimeField()

    def __str__(self):
        return self.name