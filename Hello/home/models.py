from django.db import models

# makemigration - craete changes and store in a file
# migrate- apply the pending changes created by makemigration

# Create your models here.

class Customer(models.Model):
    username = models.CharField(max_length=20)
    email = models.CharField(max_length=30)
    gender = models.CharField(max_length=10)
    age = models.IntegerField()
    phone = models.CharField(max_length=15)
    date_time = models.DateTimeField()
    
    def __str__(self):
        return self.username

class Contact(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)  # Required
    email = models.EmailField(null=False, blank=False)  # Required
    phone = models.CharField(max_length=15, null=False, blank=False)  # Required
    desc = models.TextField(null=False, blank=False)  # Required
    date = models.DateTimeField(null=False, blank=False)  # Required

    def __str__(self):
        return self.name
