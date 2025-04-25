from studentApp.models import *
import random

from faker import Faker
fake = Faker()

def generateData(n=50):
    dept = Department.objects.all()

    for i in range(n):
        d_index = random.randint(0, len(dept)-1)
        d = dept[d_index]
        fname = fake.first_name()
        lname = fake.last_name()
        age = random.randint(20,40)
        email = fake.email()
        s_id = StudentId.objects.create(student_id = f"S{random.randint(1, 9)}_{random.randint(111,999)}")

        Student.objects.create(dept=d, student_id=s_id, firstName=fname, lastName=lname, age=age, email=email)

        print(d, fname, lname, age, email, s_id)

def generateMarks(n=50):
    students = Student.objects.all()

    for s in students:
        subjects = Subject.objects.all()
        for sub in subjects:
            marks = random.randint(15,100)
            Mark.objects.create(student=s, subject=sub, marks=marks)

            print(s, sub, marks)



