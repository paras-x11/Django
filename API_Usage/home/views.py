from django.shortcuts import render, redirect, HttpResponse
from django.core.mail import BadHeaderError, send_mail
from django.core.mail import send_mail
from django.conf import settings
import razorpay
from django.http import JsonResponse


# Create your views here.
def index(request):
    return render(request, "index.html")


def mail(request):
    return render(request, "mail.html")

def sendEmail(request):
    context = {"result": "Invalid request"}  # Default response

    if request.method == 'POST':
        address = request.POST.get("email")
        subject = request.POST.get("subject")
        message = request.POST.get("message")

        print(address, subject, message)
        
        if not address or not subject or not message:
            return HttpResponse("Fill All The Details")

        try:
            send_mail(subject, message, settings.EMAIL_HOST_USER, [address])
            context["result"] = "Email sent successfully"
        except Exception as e:
            context["result"] = f"Error sending email: {e}"

    return HttpResponse(context["result"])  # Always return a valid response


def payment(request):
    return render(request, "payment.html")

def makePayment(request):
    amount = request.GET.get("amount")
    print(amount)

    client = razorpay.Client(auth=("rzp_test_wef6Tlaev3Pre9", "OeabKs2qmdPauM2RHWDQb9TG"))

    data = { "amount": int(amount)*100 , "currency": "INR", "receipt": "order_rcptid_11" }
    payment = client.order.create(data=data) 

    return JsonResponse(payment)

