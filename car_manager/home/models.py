from django.db import models


# Create your models here.

# Helper function for image upload path
def car_image_upload_path(instance, filename):
    return f'car_images/{instance.name}_{filename}'

class Car(models.Model):
    name = models.CharField(max_length=100)
    brand = models.CharField(max_length=100)
    model_year = models.PositiveIntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    color = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)
    car_image = models.ImageField(upload_to=car_image_upload_path, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.brand} ({self.name})"
