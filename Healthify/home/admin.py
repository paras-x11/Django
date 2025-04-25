from django.contrib import admin
from home.models import *

# Register your models here.
admin.site.register(User)
admin.site.register(Department)
admin.site.register(DoctorProfile)
admin.site.register(PatientProfile)
admin.site.register(Appointment)
admin.site.register(ContactMessage)