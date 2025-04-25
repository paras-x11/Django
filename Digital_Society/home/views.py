from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User


# Create your views here.
@login_required(login_url="login_user")
def index(request):
    # if request.user.is_anonymous:
    #     return redirect("login_user")
    return render(request, "index.html")

def login_user(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        print(username, password)

        if not username or not password:
            messages.error(request, "Enter All Details")
            return redirect("login_user")
        else:
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect("index")
            else:
                messages.error(request, "Invalid Username or Password")
                return redirect("login_user")
    return render(request, "login.html")

def signup_user(request):
    if request.user.is_authenticated:
        return redirect("index")
    if request.method == "POST":
        data = request.POST
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        cpassword = data.get('cpassword')

        if not username or not email or not password or not cpassword:
            messages.error(request, "Enter All The Details")
            return render(request, "signup.html")
        else:
            if password == cpassword:
                user = User(username=username, email=email)
                user.set_password(password)
                user.save()
                messages.success(request, "Registration Successfull")
                return redirect("login_user")
            else:
                messages.error(request, "Please Enter Same Password")
                return render(request, "signup.html") 
    return render(request, "signup.html")

def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Logout Succesfull")
    return render(request, "login.html")

def forgot_password(request):
    return render(request, "login.html")

@login_required(login_url="login_user")
def profile(request):
    return render(request, "profile.html")

@login_required(login_url="login_user")
def society_members(request):
    return render(request, "members.html")

@login_required(login_url="login_user")
def society_watchmens(request):
    return render(request, "watchmens.html")

@login_required(login_url="login_user")
def notice(request):
    return render(request, "notice.html")

@login_required(login_url="login_user")
def events(request):
    return render(request, "events.html")