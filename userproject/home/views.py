# password for user (paras): Paras$$$***000
# password for user (robert): Robert$$$***000
# password for user (jhon): Jhon$$$***000


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from home.models import *
from home.forms import SignupForm
from home.forms import LoginForm
from datetime import datetime

# Create your views here.
def index(request):
    if request.user.is_anonymous:
        return redirect("/login")
    
    return render(request, 'index.html')

def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                messages.success(request, "You have successfully logged in.")
                return redirect('home')  # Redirect to a home page or dashboard
            else:
                messages.error(request, "Invalid credentials.")
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = LoginForm()

    return render(request, 'login.html', {'form': form})

# def login_user(request):
#     if request.method == "POST":
#         username = request.POST.get('username')
#         password = request.POST.get('password')

#         user = authenticate(request, username=username, password=password)

#         if user is not None:
#             login(request, user)
#             return redirect("/")
#         else:
#             messages.error(request, "Invalid Username or Password")
#             return render(request, "login.html")
#     return render(request, 'login.html')

def logout_user(request):
    logout(request)
    messages.success(request, "You logged Out Succesfully")
    return redirect('/login')

def signup_user(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('login')  # Redirect to login page
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = SignupForm()

    return render(request, 'signup.html', {'form': form})

def customer(request):
    if request.user.is_anonymous:
        return redirect("/login")
    
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        age = request.POST.get('age')
        gender = request.POST.get('gender')
        phone = request.POST.get('phone')

        if not username or not email or not age or not gender or not phone:
            messages.error(request, "Fill all the details")
        else:
            Customer.objects.create(username=username, email=email, age=age, gender=gender, phone=phone, date_time=datetime.now())
            messages.success(request, "Details stored successfully.")
    return render(request, "customer.html")

def contact(request):
    if request.user.is_anonymous:
        return redirect("/login")
    
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')

        if not name or not email or not phone or not desc:
            messages.error(request, "Fill all the details")
        else:
            Contact.objects.create(name=name, email=email, phone=phone, desc=desc, date_time=datetime.now())
            messages.success(request, "Details stored successfully.")
    return render(request, "contact.html")