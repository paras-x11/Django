from django.shortcuts import render, redirect, get_object_or_404, HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from home.models import *
from django.http import JsonResponse
from django.http import Http404
from django.views.decorators.cache import never_cache
from django.forms.models import model_to_dict
from django.contrib import messages

# Create your views here.
def index(request):
    doctors = DoctorProfile.objects.all()
    context = {'doctors': doctors}
    return render(request, "index.html", context)

def get_user_info(request):
    try:
        user = request.user
        if user.is_anonymous:
            return JsonResponse({'name': 'Newbie'})
        
        name = ""
        role = ""

        if user.is_doctor:
            try:
                doctor = DoctorProfile.objects.get(user=user)
                name = doctor.full_name
                role = "Doctor"
            except DoctorProfile.DoesNotExist:
                name = "Doctor" 

        if user.is_patient:
            try:
                patient = PatientProfile.objects.get(user=user)
                name = patient.full_name
                role = "Patient"
            except DoctorProfile.DoesNotExist:
                name = "Patient"

        if user.is_superuser:
            name = f"{user.first_name} {user.last_name}"
        # print(name, role)
        return JsonResponse({'name':name, "role": role})
    except Exception as e:
        return JsonResponse({'name': ''})


def doctors(request):
    doctors = DoctorProfile.objects.all()
    context = {'doctors': doctors}
    return render(request, "doctors.html", context)

def doctor_profile(request, d_id):
    try:
        doctor = get_object_or_404(DoctorProfile, pk=d_id)
        context = {'doctor': doctor}
        return render(request, "doctor_profile.html", context)
    
    except Http404:
        return render(request, '404.html')
    except Exception as e:
        return render(request, 'doctor_profile.html', {"messgae": str(e)})
    

@never_cache
@login_required(login_url='login_user')
def appointment(request):
    doctors = DoctorProfile.objects.all()
    return render(request, "appointment.html", {'doctors': doctors})

@login_required(login_url='login_user')
def book_appointment(request):
    try:
        if request.method == "POST":
            name = request.POST.get('name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            patient = get_object_or_404(PatientProfile, user=request.user)
            doctor = get_object_or_404(DoctorProfile, pk=request.POST.get('doctor'))
            date = request.POST.get('date')
            time = request.POST.get('time')
            symptoms = request.POST.get('symptoms')

            if not all([name, email, phone, doctor, date, time, symptoms]):
                messages.error(request, "All Fields are Required!!")
                return redirect('appointment')
            
            appointment = Appointment.objects.create(
                patient=patient, doctor=doctor, a_name=name, a_email=email, 
                a_phone=phone, date=date, time=time, symptoms=symptoms
            )

            if appointment:
                messages.success(request, f"Appointment Booked on {appointment.date} at {appointment.time} with {appointment.doctor.full_name}")   
            else:
                messages.error(request, f"Something went wrong!!")   
            return redirect('appointment')
    
    except Http404:
        messages.error(request, "Something went wrong. make sure u filled the form properly!!")
        return redirect('appointment')
    except Exception as e:
        print(str(e))
        messages.error(request, "Something Went Wrong!!")
        return redirect('appointment')

@never_cache
@login_required(login_url="login_user")
def appointment_list(request):
    try:
        appointments = []  # Default fallback if no role matches

        if request.user.is_superuser:
            appointments = Appointment.objects.all()
        elif request.user.is_doctor:
            doctor = DoctorProfile.objects.get(user=request.user)
            appointments = Appointment.objects.filter(doctor=doctor)
        elif request.user.is_patient:
            patient = PatientProfile.objects.get(user=request.user)
            appointments = Appointment.objects.filter(patient=patient)
        else:
            return render(request, '404.html') 

        context = {'appointments': appointments}
        return render(request, "appointment_list.html", context)

    except Exception as e:
        print(str(e))
        return render(request, 'appointment_list.html', {"message": "Something went wrong!"})


def get_appointments(request, status):
    try:
        appointments = []
        if not status:
            return render(request, "partial/appointments_row.html", {"message": "status not matched"})
        print("STATUS:" , status)

        valid_statuses =  ('All', 'Pending', 'Approved', 'Rejected', 'Completed')
        print("check: ", status in valid_statuses)

        if status not in valid_statuses:
            return render(request, "partial/appointments_row.html", {"message": "status not matched"})

        if request.user.is_superuser:
            if status == "All":
                appointments = Appointment.objects.all()
            else:
                appointments = Appointment.objects.filter(status=status)
            return render(request, "partial/appointments_row.html", {"appointments": appointments})
        
        elif request.user.is_doctor:
            doctor = get_object_or_404(DoctorProfile, user=request.user)
            if status == "All":
                appointments = Appointment.objects.filter(doctor=doctor)
            else:
                appointments = Appointment.objects.filter(status=status, doctor=doctor)
            return render(request, "partial/appointments_row.html", {"appointments": appointments})
        
        elif request.user.is_patient:
            patient = get_object_or_404(PatientProfile, user=request.user)
            if status == "All":
                appointments = Appointment.objects.filter(patient=patient)
            else:
                appointments = Appointment.objects.filter(status=status, patient=patient)
            return render(request, "partial/appointments_row.html", {"appointments": appointments})
        
        else:
            return render(request, "partial/appointments_row.html", {"message": "Something went wrong! user not logged in"})
    except Exception as e:
        print(str(e))
        return render(request, "partial/appointments_row.html", {"message": "Something went wrong!"})


@login_required(login_url='login_user')
def appointment_detail(request, a_id):
    try:
        if request.user.is_superuser:
            appointment = get_object_or_404(Appointment, pk=a_id)
        elif request.user.is_doctor:
            doctor = DoctorProfile.objects.get(user=request.user)
            appointment = get_object_or_404(Appointment, pk=a_id, doctor=doctor)
        elif request.user.is_patient:
            patient = PatientProfile.objects.get(user=request.user)
            appointment = get_object_or_404(Appointment, pk=a_id, patient=patient)
        else:
            return render(request, '404.html') 
        
        context = { 'appointment' : appointment , 'a_id': appointment.id}
        return render(request, "appointment_detail.html", context)
    
    except Http404:
        return render(request, '404.html') 
    except Exception as e:
        print(str(e))
        return render(request, 'appointment_detail.html', {"message": "Something Went Wrong!!"})

def update_status(request):
    try:
        a_id = request.POST.get('a_id')
        print(a_id)
        status = request.POST.get('status')
        print(status)
        appointment = Appointment.objects.get(pk=a_id)
        print("status Before:", appointment.status)
        appointment.status = status
        appointment.save()
        print("status after:", appointment.status)
        return JsonResponse({'a_status': appointment.status})
    except Exception as e:
        print(str(e))
        return render(request, "appointment_detail.html", {"message": "Something Went Wrong!!"})


def about(request):
    doctors = DoctorProfile.objects.all()
    context = {'doctors': doctors}
    return render(request, "about.html", context)

def services(request):
    return render(request, "services.html")

def testimonial(request):
    return render(request, "testimonial.html")

def contact(request):
    return render(request, "contact.html")



@login_required(login_url="login_user")
def profile(request):
    user = request.user
    departments = Department.objects.all()
    context = { "departments": departments,
                "user_data": {
                    "role": "Doctor" if user.is_doctor else "Patient" if user.is_patient else "Superuser",
                    "email": user.email,
                }}

    if user.is_doctor:
        doctor = DoctorProfile.objects.get(user=user)
        context["user_data"].update({
            "firstName": doctor.first_name,
            "lastName": doctor.last_name,
            "address": doctor.address,
            "department": doctor.department,
            "specialization": doctor.specialization,
            "gender": doctor.gender,
            "phone": doctor.phone,
            "bio": doctor.bio,
            "clinicAddress": doctor.clinic_address,
            "clinicName": doctor.clinic_name,
            "image": doctor.doctor_image.url if doctor.doctor_image else "",
        })

    elif user.is_patient:
        patient = PatientProfile.objects.get(user=user)
        context["user_data"].update({
            "firstName": patient.first_name,
            "lastName": patient.last_name,
            "phone": patient.phone,
            "address": patient.address,
            "age": patient.age,
            "gender": patient.gender,
            "image": patient.patient_image.url if patient.patient_image else "",
        })

    elif user.is_superuser:
        context["user_data"].update({
            "firstName": user.first_name or user.username,
            "lastName": user.last_name or "",
            "phone": "-",  # Optional fields
            "address": "-",
            "gender": "-",
            "image": "",  # You can set default admin image
        })
    return render(request, "profile.html", context)

def update_profile(request):
    if request.method == "POST":
        data = request.POST
        files = request.FILES
        Image = files.get('profile_image')
        Email = data.get('email')
        Phone = data.get('phone')
        Address = data.get('address')
        FirstName = data.get('firstname')
        LastName = data.get('lastname')
        Gender = data.get('gender')
        Age = data.get('age')
        print("Common data: ", Email, Phone, Address, FirstName, LastName, Gender, Age)

        user = request.user
        print(user)

        if user.is_doctor:
            doctor = get_object_or_404(DoctorProfile, user=user)
            print(doctor)
            DepaermentId = data.get('department')
            Specialization = data.get('specialization')
            Bio = data.get('bio')
            ClinicName = data.get('clinicname')
            ClinicAddress = data.get('clinicaddress')
            print("Doctors: ", Email, Phone, Address, FirstName, LastName,  Gender, Age, Department, Specialization, Bio, ClinicName, ClinicAddress)

            user.email = Email
            user.save()
            if DepaermentId:
                dept = Department.objects.get(pk=DepaermentId)
                doctor.department = dept
            doctor.first_name = FirstName
            doctor.last_name = LastName
            doctor.address = Address
            doctor.specialization = Specialization
            doctor.gender = Gender
            doctor.phone = Phone
            doctor.bio = Bio
            doctor.clinic_name = ClinicName
            doctor.clinic_address = ClinicAddress
            if Image:
               doctor.doctor_image = Image
            doctor.save()
            return JsonResponse({"status": "ok"})
        
        if user.is_patient:
            patient = get_object_or_404(PatientProfile, user=user)
            print(patient)
            user.email = Email
            user.save()
            patient.first_name = FirstName
            patient.last_name = LastName
            patient.age = Age
            patient.gender = Gender
            patient.phone = Phone
            patient.address = Address
            if Image:
                patient.patient_image = Image
            patient.save()
            return JsonResponse({"status": "ok"})
        
        if user.is_superuser:
            user.email = Email
            user.first_name = FirstName
            user.last_name = LastName
            user.save()
            return JsonResponse({"status": "ok"})
            
    return JsonResponse({"status": "failed"})



def signup_user(request):
    try:
        if request.method == "POST":
            role = request.POST.get('role')
            fname = request.POST.get('first_name')
            lname = request.POST.get('last_name')
            email = request.POST.get('email')
            phone = request.POST.get('phone')
            password = request.POST.get('password')

            is_email_exist = User.objects.filter(email=email)
            if is_email_exist:
                return render(request, 'signup.html', {"message":'Email already exist !!'})
            
            user = User.objects.create_user(
                email=email,
                password=password,
                is_doctor=(role == "Doctor"),
                is_patient=(role == "Patient")
            )

            if role == "Doctor":
                doctor = DoctorProfile.objects.create(user=user, first_name=fname, last_name=lname, phone=phone)
                print(doctor)
            if role == "Patient":
                patient = PatientProfile.objects.create(user=user, first_name=fname, last_name=lname, phone=phone)
                print(patient)

            return render(request, "login.html", {"message": f'{role} Registration Succesfull, Login Now!!'})
        return render(request, "signup.html")
    except Exception as e:
        return render(request, 'signup.html', {"message": str(e)})

def login_user(request):
    try:
        if request.method=="POST":
            email = request.POST.get('email')
            password = request.POST.get('password')

            user = authenticate(email=email, password=password)
            if user:
                login(request, user)
                return redirect(index)
            else:
                return render(request, 'login.html', {"message": 'Invalid Credential !! '})

        return render(request, "login.html")
    except Exception as e:
        return render(request, 'login.html', {"messgae": str(e)})
    
@login_required(login_url='login_user')
def logout_user(request):
    if request.user.is_authenticated:
        logout(request)
        return render(request, 'login.html', {'message': "Logout Succesfull"})
    else:
        return render(request, 'index.html')

    