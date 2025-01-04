# password for user (paras): Paras$$$***000
# password for user (robert): Robert$$$***000
# password for user (jhon): Jhon$$$***000


from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from home.models import *
from home.forms import SignupForm
from home.forms import LoginForm

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