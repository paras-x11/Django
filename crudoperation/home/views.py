from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from home.models import *


# Create your views here.
def index(request):
    if request.user.is_anonymous:
        return redirect("login")
    return render(request, "index.html")

def signup_user(request):
    if request.user.is_authenticated:
        return redirect("index")
    
    if request.method == "POST":
        uname = request.POST.get("uname")
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        email = request.POST.get("email")
        password = request.POST.get("pass")

        if not uname or not fname or not lname or not email or not password:
            messages.error(request, "Fill all details.")
        else:
            user = User.objects.create(username=uname, first_name=fname, last_name=lname, email=email)
            user.set_password(password)
            user.save()
            messages.success(request, "Registration Succesfull !!!")
            return redirect("login")
    return render(request, "signup.html")

def login_user(request):
    # if not request.user.is_anonymous:
    #     return redirect("index")
    
    if request.user.is_authenticated:
        return redirect("index")
    
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        if not username or not password:
            messages.error(request, "Fill all details")
            return redirect("login")
        else:
            user = authenticate(request, username=username, password=password)

            if user:
                login(request, user)
                return redirect("index")
            else:
                messages.error(request, "Enter correct details")
                return redirect("login")
    return render(request, "login.html")

def logout_user(request):
    logout(request)
    return redirect("login")

@login_required(login_url="login")
def userform(request):
    allusers = MyUser.objects.all()

    return render(request, "userform.html", {"users" : allusers})

def adduser(request):
    if request.user.is_anonymous:
        return redirect("login")
    
    allusers = MyUser.objects.all()

    if request.method == "POST":
        id = request.POST.get("id")
        username = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        if not username or not email or not phone:
            messages.error(request, "Fill All Details.")
            return redirect("userform")
        else:
            if id:
                cuser = MyUser.objects.get(pk=id)
                cuser.username = username
                cuser.email = email
                cuser.phone = phone
                cuser.save()
                messages.success(request, "User Updated Successfully !!!")
            else:
                MyUser.objects.create(username=username, email=email, phone=phone)
                messages.success(request, "User Added Successfully !!!")
    return redirect("userform")

def edituser(request, id):
    u = MyUser.objects.get(pk=id)
    allusers = MyUser.objects.all()
    return render(request, "userform.html", {"u": u, "users":allusers})

def deleteuser(request, id):
    user = MyUser.objects.get(pk=id)
    user.delete()
    return redirect("userform")

