# password for user(robert): Robert$$$@999

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

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
            # Login the user
            login(request, user)
            return redirect("/")  # Redirect to home page (or dashboard)
        else:
            # Invalid credentials, show an error message
            messages.error(request, "Invalid username or password.")
            return render(request, "login.html")
        
    return render(request, 'login.html')

# Logout view
def logout_user(request):
    logout(request)
    return redirect("/login")
