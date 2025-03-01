
from django.shortcuts import render,redirect
from django.contrib.auth.decorators import login_required


# Create your views here.
login_required(login_url="login_user")
def index(request):
    if request.user.is_anonymous:
        redirect("login_user")
    return render(request, "index.html")

def login_user(request):
    return render(request, "login.html")

def signup_user(request):
    return render(request, "signup.html")