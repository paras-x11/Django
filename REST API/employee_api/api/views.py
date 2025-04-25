from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializer import EmployeeSerializer
from api.models import *


# Create your views here.
@api_view(['GET'])
def getEmployees(request):
    allemployees = Employee.objects.all()
    e_data = EmployeeSerializer(allemployees, many=True)
    return Response(e_data.data)

@api_view(['POST'])
def addEmployee(request):
    serialize_data = EmployeeSerializer(data = request.data)
    if not serialize_data.is_valid():
        return Response({'status':'202','errors':serialize_data.errors,'message':"something went wrong"})
    serialize_data.save()
    return Response({'status':'200','data':serialize_data.data ,'message':"Student Added"})

@api_view(['PATCH'])
def updateEmployee(request, id):
    try:
        employee = Employee.objects.get(pk=id)

        s_data = EmployeeSerializer(employee, request.data, partial=True)
        if not s_data.is_valid():
            return Response({'status':'202','errors':s_data.errors,'message':"something went wrong"})
        s_data.save()
        return Response({'status':'200','data':s_data.data ,'message':"Student Updated"})
    except Exception as e:
        return Response({'status':'202','errors':str(e) ,'message':"something went wrong"})

@api_view(['DELETE'])
def deleteEmployee(request, id):
    try:
        employee = Employee.objects.get(pk=id)

        s_data = EmployeeSerializer(employee)
        if not employee:
            return Response({'status':'202','errors':s_data.errors,'message':"Employee not found"})
        employee.delete()
        return Response({'status':'200','data':s_data.data ,'message':"Student Deleted"})
    except Exception as e:
        return Response({'status':'202','errors':str(e) ,'message':"something went wrong"})
