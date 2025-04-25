from django.shortcuts import render
from studentApp.models import *
from django.core.paginator import Paginator
from django.db.models import Sum

# Create your views here.
def index(request):
    students = Student.objects.all()
    paginator = Paginator(students, 25)  # Show 25 contacts per page.

    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    return render(request, "index.html", {"students": page_obj})

def marks(request, id):
    # student = Student.objects.get(student_id__student_id=id)  # Fetch the student by student_id
    # studentMarks = Mark.objects.filter(student=student)  # Get all marks for the student

    ranks = Student.objects.annotate(totalmarks= Sum("mark__marks")).order_by("-totalmarks")
    count = 0
    for i in ranks:
        count += 1
        if i.student_id.student_id == id:
            rank = count
            break
    
    studentMarks = Mark.objects.filter(student__student_id__student_id = id)
    std = studentMarks[0].student
    total = studentMarks.aggregate(total = Sum("marks"))
        
    return render(request, "marks.html", {'student': std, 'studentMarks': studentMarks, "total":total, "rank":rank})