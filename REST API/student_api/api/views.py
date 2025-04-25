from django.shortcuts import render, HttpResponse
from rest_framework.decorators import api_view
from rest_framework.response import Response
from api.serializer import StudentSerializer
from api.models import *


# Create your views here.
@api_view(['GET'])
def getStudents(request):
    allstudents = Student.objects.all()
    s_data = StudentSerializer(allstudents,     many=True)
    print(s_data)
    return Response(data = s_data.data)

@api_view(['POST'])
def addStudent(request):
    serialize_data = StudentSerializer(data = request.data)
    if not serialize_data.is_valid():
        return Response({'status':'202','errors':serialize_data.errors,'message':"something went wrong"})
    serialize_data.save()
    return Response({'status':'200', 'data':serialize_data.data, 'message':'Student Added'})

@api_view(['patch'])
def updateStudent(request, id):
    try:
        student = Student.objects.get(pk=id)
        s_data = StudentSerializer(student, request.data, partial=True)
        if not s_data.is_valid():
            return Response({'status':'202', 'errors':s_data.errors, 'message':'Something Went Wrong'})
        s_data.save()
        return Response({'status':'200', 'data':s_data.data, 'message':'Student Updated'})
    except Exception as e:
        return Response({'status':'202', 'errors':str(e), 'message':'Something went wrong'})
    
@api_view(['delete'])
def deleteStudent(request, id):
    try:
        student = Student.objects.get(pk=id)
        s_data = StudentSerializer(student)
        if not student:
            return Response({'status':'202', 'errors':s_data.errors, 'message':'Something Went Wrong'})
        student.delete()
        return Response({'status':'200', 'data':s_data.data, 'message':'Student Deleted'})
    except Exception as e:
        return Response({'status':'202', 'errors':str(e), 'message':'Something went wrong'})