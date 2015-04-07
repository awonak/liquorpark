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
    status = None
    msg = None
    # form submission
    if request.method == "POST":
        # send email to team@drinkliquorpark.com
        sg = sendgrid.SendGridClient(
            os.getenv('SENDGRID_USERNAME'),
            os.getenv('SENDGRID_PASSWORD')
        )
        message = sendgrid.Mail()
        message.add_to('team@drinkliquorpark.com')
        message.set_subject('Contact Submission from drinkliquorpark.com')
        message.set_text(request.POST.get('message'))
        message.set_from(request.POST.get('from'))
        status, msg = sg.send(message)
        if status == 200:
            return redirect('contact-thanks')

    return render(request, 'contact.html', msg)


def contact_thanks(request):
    return render(request, 'contact-thanks.html')


def events(request):
    return render(request, 'events.html')


def margincalc(request):
    return render(request, 'margincalc.html')
