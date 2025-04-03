"""
URL configuration for email_project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
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
