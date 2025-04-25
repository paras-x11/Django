from django.db import models
from django.contrib.auth.models import AbstractUser, PermissionsMixin 
from home.manager import CustomUserManager 


# -------------------------------
# Custom User Model
class User(AbstractUser, PermissionsMixin):
    username = None
    email = models.EmailField(unique=True)
    is_doctor = models.BooleanField(default=False)
    is_patient = models.BooleanField(default=False)

    REQUIRED_FIELDS  = []
    USERNAME_FIELD = 'email'

    objects = CustomUserManager()

    def __str__(self):
        return f"{self.username} - {self.email}"

# -------------------------------
# Department Model
class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    

# -------------------------------
# Doctor Profile  
class DoctorProfile(models.Model):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    department = models.ForeignKey(Department, on_delete=models.SET_NULL, null=True, related_name='doctors')  # added
    doctor_image = models.ImageField(upload_to="doctor_images", height_field=None, width_field=None, max_length=None, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.TextField(blank=True, null=True)
    specialization = models.CharField(max_length=100, null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True)
    phone = models.CharField(max_length=15, unique=True)
    bio = models.TextField(blank=True)
    clinic_name = models.CharField(max_length=100, blank=True)
    clinic_address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} - {self.last_name}"
    
    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

# -------------------------------
# Patient Profile
class PatientProfile(models.Model):
    GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    patient_image = models.ImageField(upload_to="patient_images", height_field=None, width_field=None, max_length=None, null=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    age = models.PositiveIntegerField(null=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, null=True)
    phone = models.CharField(max_length=15, unique=True, null=True)
    address = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} - {self.last_name}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

# -------------------------------
# Appoint Model
class Appointment(models.Model):
    STATUS_CHOICES = [('Pending', 'Pending'), ('Approved', 'Approved'),
                      ('Rejected', 'Rejected'), ('Completed', 'Completed')]
    
    patient = models.ForeignKey(PatientProfile, on_delete=models.CASCADE)
    doctor = models.ForeignKey(DoctorProfile, on_delete=models.CASCADE)
    a_name = models.CharField(max_length=100, blank=True)               # appointment name
    a_email = models.EmailField(max_length=100, blank=True)             # appointment email
    a_phone = models.CharField(max_length=15, blank=True)               # appointment phone
    date = models.DateField()
    time = models.TimeField()
    symptoms = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.patient.full_name} - {self.doctor.full_name}"

# -------------------------------
# Contact or Feedback 
class ContactMessage(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=150)
    message = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.subject