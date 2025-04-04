from django.contrib import admin
from django.urls import path
from django.urls import path, include
from django.urls import path
from email_app.views import fetch_inbox, send_email, fetch_sent_emails, email_sent

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('email_app.urls')),
    path("inbox/", fetch_inbox, name="inbox"),
    path('send_email/', send_email, name='send_email'),
    path("sent/", fetch_sent_emails, name="sent_emails"),
    path('email_sent/', email_sent, name='email_sent'),  

]
