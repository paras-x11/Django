from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from home.models import *
from django.db.models import Q

# Create your views here.
def index(request):
    return render(request, "index.html")

def addUser(request):
    if request.method == "POST":
        uname = request.POST.get("uname")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        print(uname, email, phone)

        if not uname or not email or not phone:
            return HttpResponse("Enter All Details")
        else:
            MyUser.objects.create(username=uname, email=email, phone=phone)
        return HttpResponse("User Registered Successfully")    

def viewUser(request):
    allUsers = MyUser.objects.all()
    print(allUsers)
    return JsonResponse({"allUsers" : list(allUsers.values())})

def getData(request):
    id = request.GET.get("uid")
    cuser = MyUser.objects.get(pk=id)
    cu = {
        "id" : cuser.id,
        "username" : cuser.username,
        "email" : cuser.email,
        "phone" : cuser.phone
    }
    return JsonResponse({"cu" : cu})    

def updateUser(request):
    if request.method == "POST":
        id = request.POST.get("id")
        uname = request.POST.get("uname")
        email = request.POST.get("email")
        phone = request.POST.get("phone")

        if not uname or not email or not phone:
            return HttpResponse("Enter All Details - Try Again")
        else:
            if id:
                cu = MyUser.objects.get(pk=id)
                cu.username = uname
                cu.email = email
                cu.phone = phone
                cu.save()
            else:
                return HttpResponse("Try Again")
        return HttpResponse("User Updated Successfully")

def deleteUser(request):
    id = request.GET.get("uid")
    cu = MyUser.objects.get(pk=id)
    cu.delete()
    return HttpResponse("User Deleted Successfully")

def searchUser(request):
    if request.method == "GET":
        data = request.GET.get("data")
        print(data)
        result = MyUser.objects.filter(
            Q (username__startswith = data) |
            Q (email__startswith = data)    |
            Q (phone__startswith = data))
        return JsonResponse({"result" : list(result.values())})