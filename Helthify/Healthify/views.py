
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Doctor, Patient, Appointment

def home(request):
    return render(request, 'healthify/home.html')

def register(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        email = request.POST.get('email')
        role = request.POST.get('role')  # Either 'doctor' or 'patient'
        try:
            user = User.objects.create_user(username=username, password=password, email=email)
            if role == 'doctor':
                specialization = request.POST.get('specialization')
                Doctor.objects.create(user=user, specialization=specialization, contact=request.POST.get('contact'), bio=request.POST.get('bio'))
            elif role == 'patient':
                Patient.objects.create(user=user, contact=request.POST.get('contact'))
            return redirect('login')
        except Exception as e:
            return render(request, 'healthify/register.html', {'error': str(e)})
    return render(request, 'healthify/register.html')

def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'healthify/login.html', {'error': 'Invalid credentials'})
    return render(request, 'healthify/login.html')

def logout_user(request):
    logout(request)
    return redirect('home')

@login_required
def profile(request):
    if hasattr(request.user, 'doctor'):
        profile = request.user.doctor
        role = 'doctor'
    elif hasattr(request.user, 'patient'):
        profile = request.user.patient
        role = 'patient'
    else:
        profile = None
        role = None
    return render(request, 'healthify/profile.html', {'profile': profile, 'role': role})

@login_required
def manage_appointments(request):
    if hasattr(request.user, 'doctor'):
        appointments = Appointment.objects.filter(doctor=request.user.doctor)
    elif hasattr(request.user, 'patient'):
        appointments = Appointment.objects.filter(patient=request.user.patient)
    else:
        appointments = []
    return render(request, 'healthify/appointments.html', {'appointments': appointments})
