from django.shortcuts import render, HttpResponse, redirect
from home.models import *
from django.http import JsonResponse
from django.contrib import messages

# Create your views here.
def index(request):
    return render(request, "index.html")

def addStudent(request):
    if request.method == "POST":
        data = request.POST
        uname = data.get("uname")
        email = data.get("email")
        phone = data.get("phone")
        print(uname, email, phone)

        if not uname or not email or not phone:
            return HttpResponse("Please Enter All The Details")
        else:
            Student.objects.create(username=uname, email=email, phone=phone)
    return HttpResponse("Registration Successfull")

def viewStudent(request):
    allStudents = Student.objects.all()
    return JsonResponse({"allStudents" : list(allStudents.values())})

def edit(request):
    id = request.GET.get("uid")
    print(id)
    st = Student.objects.filter(id=id)
    return JsonResponse({"st" : list(st.values())})

def updateStudent(request):
    if request.method == "POST":
        data = request.POST
        id = data.get("id")
        uname = data.get("uname")
        email = data.get("email")
        phone = data.get("phone")
        print(uname, email, phone)

        if not uname or not email or not phone:
            return HttpResponse("Details can't be empty - Try Again")
        else:
            if id:
                st = Student.objects.get(pk=id)
                st.username = uname
                st.email = email
                st.phone = phone
                st.save()
    return HttpResponse("Student Updated Successfully")

def deleteStudent(request):
    id = request.GET.get('uid')
    st = Student.objects.get(pk=id)
    st.delete()
    return HttpResponse("Student Deleted Succesfully")

def searchStudent(request):
    data = request.GET.get('data')
    print(data)
    allStudents = Student.objects.filter(username__startswith=data)
    return JsonResponse({"allStudents" : list(allStudents.values())})
