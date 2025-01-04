from django.shortcuts import render, HttpResponse
from datetime import datetime
from home.models import *
from django.contrib import messages


# Create your views here.

def demo(request):
    context = {
        "variable" : "I am variable 007",
        "variable1" : "Paras",
        "variable2" : "Rana"
    }
    return render(request, 'demo.html', context)
    # return HttpResponse("HELLO WORLD! \n \n Index Page")

def index(request):
    return render(request, 'index.html')
    # return HttpResponse("HELLO WORLD! \n \n Index Page")

def about(request):
    return render(request, 'about.html')

def services(request):
    return render(request, 'services.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        desc = request.POST.get('desc')

        # Validate input fields
        if not name or not email or not phone or not desc:
            messages.error(request, 'All fields are required.')
        else:
            contact = Contact(name=name, email=email, phone=phone, desc=desc, date=datetime.today())
            contact.save()
            messages.success(request, 'Your contact request has been submitted successfully!')

    return render(request, 'contact.html')

def customer(request):
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        gender = request.POST.get('gender')
        age = request.POST.get('age')
        phone = request.POST.get('phone')

        if not username or not email or not gender or not age or not phone:   
            messages.error(request, "All fields are required")
        
        else:
            customer = Customer(username=username, email=email, gender=gender, age=age, phone=phone, date_time=datetime.now())
            customer.save()
            messages.success(request, 'Your Details has been submitted successfully!')

    return render(request, "customer.html")



