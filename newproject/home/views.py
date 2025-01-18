# password for user(rohit): rohit@@@###000

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from home.models import *

# Home page view
def index(request):
    if request.user.is_anonymous:
        return redirect("/login")
    return render(request, 'index.html')

# Login view
def login_user(request):
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            return redirect("/")  # Redirect to home page (or dashboard)
        else:
            messages.error(request, "Invalid username or password.")
            return render(request, "login.html")
        
    return render(request, 'login.html')

# Logout view
def logout_user(request):
    logout(request)
    return redirect("/login")

def userform(request):
    if request.user.is_anonymous:
        return redirect("/login")
    else:
        allusers = MyUser.objects.all()
        return render(request, "userform.html", {"users":allusers})

def adduser(request):
    if request.method == "POST":
        id = request.POST['id']
        name = request.POST['name']
        email = request.POST['email']
        phone = request.POST['phone']

        if not name or not email or not phone:
            messages.error(request, "Fill all the details")

        else:
            if id:
                cuser = MyUser.objects.get(pk=id)
                cuser.name = name
                cuser.email = email
                cuser.phone = phone
                cuser.save()
                messages.success(request, "Details updated successfully")
            else:
                MyUser.objects.create(name=name, email=email, phone=phone)
                messages.success(request, "Details stored successfully")
    return redirect("/userform")

def edituser(request, id):
    u = MyUser.objects.get(pk=id)
    alluser = MyUser.objects.all()
    return render(request, "userform.html", {"u": u, "users": alluser})

def deleteuser(request, id):
    u = MyUser.objects.get(pk=id)
    u.delete()
    return redirect("/userform")