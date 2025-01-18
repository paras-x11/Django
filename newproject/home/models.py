from django.db import models

# Create your models here.
class MyUser(models.Model):
    name = models.CharField(max_length=30)
    email = models.CharField(max_length=30)
    phone = models.CharField(max_length=30)

    def __str__(self):
        return self.name
