from django.db import models

# Create your models here.

class Chairman(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    date_of_birth = models.DateField()
    address = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
    
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    event_date = models.DateTimeField()
    location = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# class Member(models.Model):
#     user = models.OneToOneField('User', on_delete=models.CASCADE)
#     membership_date = models.DateField(auto_now_add=True)
#     status = models.CharField(max_length=20, choices=[('active', 'Active'), ('inactive', 'Inactive')])

#     def __str__(self):
#         return f"{self.user.first_name} {self.user.last_name}"

# class Notice_View(models.Model):
#     member = models.ForeignKey(Member, on_delete=models.CASCADE)
#     notice = models.ForeignKey('Notice', on_delete=models.CASCADE)
#     viewed_at = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"Notice {self.notice.title} viewed by {self.member.user.first_name} {self.member.user.last_name}"

class Notice(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    posted_by = models.ForeignKey('Chairman', on_delete=models.CASCADE)
    posted_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

# class Transaction(models.Model):
#     member = models.ForeignKey(Member, on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     transaction_date = models.DateTimeField(auto_now_add=True)
#     transaction_type = models.CharField(max_length=50, choices=[('payment', 'Payment'), ('donation', 'Donation')])
#     status = models.CharField(max_length=20, choices=[('completed', 'Completed'), ('pending', 'Pending')])

#     def __str__(self):
#         return f"{self.transaction_type} - {self.member.user.first_name}"

# from django.contrib.auth.models import AbstractUser

# class User(AbstractUser):
#     profile_picture = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
#     date_of_birth = models.DateField()
#     address = models.TextField()

#     def __str__(self):
#         return self.username

class Visitor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone_number = models.CharField(max_length=15)
    visit_date = models.DateTimeField(auto_now_add=True)
    purpose_of_visit = models.TextField()

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Watchmen(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    contact_number = models.CharField(max_length=15)
    shift_timings = models.CharField(max_length=100)  # e.g., "9 AM - 5 PM"
    assigned_area = models.CharField(max_length=200)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
