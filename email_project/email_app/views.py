from django.shortcuts import render
from .forms import EmailForm
import smtplib
import ssl
import os
from email.message import EmailMessage
from django.conf import settings

def send_email(request):
    if request.method == 'POST':
        form = EmailForm(request.POST, request.FILES)
        if form.is_valid():
            email_sender = form.cleaned_data['email_sender']
            email_receivers = form.cleaned_data['email_receivers'].split(',')
            cc_receivers = form.cleaned_data['cc_receivers'].split(',')
            subject = form.cleaned_data['subject']
            body = form.cleaned_data['body']
            attachment = request.FILES.get('attachment')

            # Create Email Message
            em = EmailMessage()
            em["From"] = email_sender
            em["To"] = ", ".join(email_receivers)
            em["Cc"] = ", ".join(cc_receivers)
            em["Subject"] = subject
            em.set_content(body)

            # Attach the file if provided
            if attachment:
                file_data = attachment.read()
                file_name = attachment.name
                em.add_attachment(file_data, maintype="application", subtype="octet-stream", filename=file_name)

            # Send Email using SMTP
            context = ssl.create_default_context()
            with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
                smtp.login(email_sender, settings.APP_PASSWORD)
                smtp.send_message(em)
                
            return render(request, 'email_app/email_sent.html', {'email': email_sender})
    else:
        form = EmailForm()
    return render(request, 'email_app/send_email.html', {'form': form})
