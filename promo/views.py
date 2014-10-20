import os
import sendgrid
from django.shortcuts import render, redirect


def index(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def proprietors(request):
    return render(request, 'proprietors.html')

def contact(request):
    # form submission
    if request.method == "POST":
        # send email to shop@drinkliquorpark.com
        sg = sendgrid.SendGridClient(
            os.getenv('SENDGRID_USERNAME'),
            os.getenv('SENDGRID_PASSWORD')
        )
        message = sendgrid.Mail(
            to='shop@drinkliquorpark.com',
            subject='Website Inquiry',
            html=request.POST.get('message'),
            text=request.POST.get('message'),
            from_email=request.POST.get('from')
        )
        status, msg = sg.send(message)
        return redirect('contact-thanks')

    return render(request, 'contact.html')

def contact_thanks(request):
    return render(request, 'contact-thanks.html')

