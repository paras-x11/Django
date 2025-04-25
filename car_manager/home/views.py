from django.shortcuts import render, redirect, get_object_or_404
from home.models import *
from django.contrib import messages
from django.http import Http404
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request, "index.html")


def car_list(request):
    cars = Car.objects.all()
    return render(request, "car_list.html", {'cars': cars})


def getCars(request):
    if request.method == "GET":
        query = request.GET.get('query')
        brand = request.GET.get('brand')
        print(query, brand)

        cars = Car.objects.all()
        if query and query != 'all':
            cars = cars.filter( Q(name__startswith=query) | Q(brand__startswith=query) | Q(color__startswith=query))
            
        if brand and brand != 'all':
            cars = cars.filter( brand__iexact=brand )
        
        print(cars)
        return render(request, 'partial/car_table.html', {"cars": cars})
    return redirect('car_list')




def car_form(request):
    return render(request, "car_form.html")


def add_car(request):
    if request.method == "POST":
        data = request.POST
        id = data.get('id')
        name = data.get('name')
        brand = data.get('brand')
        model_year = data.get('model_year')
        price = data.get('price')
        color = data.get('color')
        description = data.get('description')
        car_image = request.FILES.get('car_image')

        if id:
            print("in update")
            car = Car.objects.get(pk=id)
            print(car)
            car.name = name
            car.brand = brand
            car.model_year = model_year
            car.price = price
            car.color = color
            car.description = description
            if car_image:
                car.car_image = car_image
                car.save()
            messages.success(request, "Car Updated Succesfully!")
            return redirect('car_form')
        else:
            if not all([name, brand, model_year, price, color, description, car_image]):
                messages.error(request, "All fields required!")

            car = Car.objects.create(name=name, brand=brand, model_year=model_year,
                                     price=price, color=color, description=description, car_image=car_image)
            messages.success(request, "Car added succesfully!")
        return redirect('car_form')
    return redirect('car_form')


def car_detail(request, id):
    car = get_object_or_404(Car, pk=id)
    return render(request, 'car_detail.html', {'car': car})


def edit_car(request, id):
    try:
        car = get_object_or_404(Car, pk=id)
        return render(request, 'car_form.html', {'car': car})
   
    except Http404:
        messages.error(request, "Car Not Exist!")
        return redirect('car_list')

    except Exception as e:
        messages.error(request, f"{str(e)}")
        return redirect('car_list')


def delete_car(request, id):
    try:
        car = get_object_or_404(Car, pk=id)
        car.delete()
        messages.success(request, "Car deleted succesfully!")
        return redirect('car_list')
    
    except Http404:
        messages.error(request, "Car Not Exist!")
        return redirect('car_list')

    except Exception as e:
        messages.error(request, f"{str(e)}")
        return redirect('car_list')


def about(request):
    return render(request, 'about.html')
