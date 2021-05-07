"""cms URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.urls import path
from . import views
from CMSBEFORE.views import *
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('', views.home, name="home"),
    path('conference', views.conference, name="conference"),
    path('overview', views.overview, name="overview"),
    path('contact', views.contact_us, name="contact"),
    path('privacy', views.privacy, name="privacy"),
    path('policy', views.policy, name="policy"),
    path('feedback', views.feedback, name="feedback"),
    path('login', views.handle_login, name="login"),
    path('register', views.register, name="register"),
    path('logout', views.handle_logout, name="logout"),
    path('registrationtxt', views.registrationtext, name="registrationtxt"),
    path('confirmRegistrationtxt/<email>/<int:random1>/<int:random2>', views.ConfirmRegisterTXT, name="confirmRegistrationtxt"),

    path('reset_password/',
         auth_views.PasswordResetView.as_view(template_name="password_reset.html"),
         name="reset_password"),

    path('reset_password_sent/',
         auth_views.PasswordResetDoneView.as_view(template_name="password_reset_sent.html"),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name="password_reset_form.html"),
         name="password_reset_confirm"),

    path('reset_password_complete/',
         auth_views.PasswordResetCompleteView.as_view(template_name="password_reset_done.html"),
         name="password_reset_complete"),
]
