from django.shortcuts import render, redirect
from .forms import EmailForm
import smtplib
import ssl
import os
import email
from email.message import EmailMessage
from django.contrib import messages
from django.shortcuts import render
import imaplib
import pytz
from email.utils import parsedate_to_datetime
from django.conf import settings

def fetch_inbox(request):
    user = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD
    imap_url = "imap.gmail.com"

    try:
        con = imaplib.IMAP4_SSL(imap_url)
        con.login(user, password)
        con.select("Inbox")

        result, data = con.search(None, "ALL")
        email_ids = data[0].split()

        email_list = []
        toronto_tz = pytz.timezone("America/Toronto")  

        for num in email_ids[-10:]:  
            result, msg_data = con.fetch(num, "(RFC822)")
            if result == "OK":
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        date_str = msg["Date"]
                        parsed_date = parsedate_to_datetime(date_str)

                        if parsed_date and parsed_date.tzinfo is not None:
                            parsed_date = parsed_date.astimezone(toronto_tz)  
                        else:
                            parsed_date = toronto_tz.localize(parsed_date)  

                        email_list.append({
                            "from": msg["From"],
                            "subject": msg["Subject"],
                            "date": parsed_date.strftime("%Y-%m-%d %H:%M:%S")  
                        })

        con.close()
        con.logout()

        email_list.sort(key=lambda x: x["date"], reverse=True)

        return render(request, "email_app/inbox.html", {"emails": email_list})

    except Exception as e:
        return render(request, "email_app/inbox.html", {"error": str(e)})


def fetch_sent_emails(request):
    user = settings.EMAIL_HOST_USER
    password = settings.EMAIL_HOST_PASSWORD
    imap_url = "imap.gmail.com"

    try:
        con = imaplib.IMAP4_SSL(imap_url)
        con.login(user, password)
        con.select('"[Gmail]/Sent Mail"')

        result, data = con.search(None, "ALL")
        email_ids = data[0].split()

        sent_emails = []
        toronto_tz = pytz.timezone("America/Toronto")  

        for num in email_ids[-10:]:  
            result, msg_data = con.fetch(num, "(RFC822)")
            if result == "OK":
                for response_part in msg_data:
                    if isinstance(response_part, tuple):
                        msg = email.message_from_bytes(response_part[1])
                        date_str = msg["Date"]
                        parsed_date = parsedate_to_datetime(date_str)

                        if parsed_date and parsed_date.tzinfo is not None:
                            parsed_date = parsed_date.astimezone(toronto_tz)  
                        else:
                            parsed_date = toronto_tz.localize(parsed_date)  

                        sent_emails.append({
                            "to": msg["To"],
                            "subject": msg["Subject"],
                            "date": parsed_date.strftime("%Y-%m-%d %H:%M:%S")  
                        })

        con.close()
        con.logout()

        sent_emails.sort(key=lambda x: x["date"], reverse=True)

        return render(request, "email_app/sent.html", {"sent_emails": sent_emails})

    except Exception as e:
        return render(request, "email_app/sent.html", {"error": str(e)})

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
                em.add_attachment(file_data, maintype="application",
                                   subtype="octet-stream", filename=file_name)

            # Send Email using SMTP
            context = ssl.create_default_context()
            try:
                with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
                    smtp.login(email_sender, settings.APP_PASSWORD)
                    smtp.send_message(em)
                
                messages.success(request, "Email sent successfully!")
                return redirect('email_sent')  # Redirect to the success page
            except Exception as e:
                messages.error(request, f"Failed to send email: {e}")
                return redirect('send_email')  # Stay on the send email page if there's an error
    else:
        form = EmailForm()

    return render(request, 'email_app/send_email.html', {'form': form})

def email_sent(request):
    return render(request, 'email_app/email_sent.html') 
