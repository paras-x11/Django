
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import CustomUser

# Create your views here.
# login_required(login_url="login_user")
def index(request):
    if request.user.is_anonymous:
        return redirect("login_user")
    return render(request, "index.html")

def login_user(request):
    if request.method == "POST":
        phone = request.POST.get('phone')
        password = request.POST.get('pass')  

        user = authenticate(phone_number=phone, password=password)

        if user:
            login(request, user)
            return redirect("index")
        else:
            return render(request, "login.html")
    return render(request, "login.html")

def signup_user(request):
    if request.method == "POST":
        fname = request.POST.get('fname')
        phone = request.POST.get('phone')
        password = request.POST.get('pass')

        if CustomUser.objects.filter(phone_number=phone).exists():
            return render(request, "signup.html", {"error": "Phone number already registered!"})

        user = CustomUser.objects.create_user(phone_number=phone, password=password)
        user.first_name = fname
        user.save()

        login(request, user)  # Log in the user after signup
        return redirect("index")

    return render(request, "signup.html")

def logout_user(request):
    logout(request)
    return render(request, "login.html")
