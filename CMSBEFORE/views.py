from django.shortcuts import render, redirect
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from .models import *
from core.settings import EMAIL_HOST_USER
from django.core.mail import send_mail
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.sites.shortcuts import get_current_site
import random

User = get_user_model()


# Create your views here.


def register(request):
    if request.method == 'POST':
        fname = request.POST.get("fname")
        lname = request.POST.get("lname")
        org = request.POST.get("org")
        country = request.POST.get("country")
        region = request.POST.get("region")
        page = request.POST.get("webpage")
        usertype = request.POST.get("usertype")
        topic = request.POST.get("topic")
        if topic:
            pass
        else:
            topic = ''
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")

        users = User.objects.filter(username=username).all().count()
        if users > 0:
            messages.error(request, "THIS username IS ALREADY ASSOCIATED WITH ANOTHER ACCOUNT Try Again")
            return redirect('home')
        else:
            users = User.objects.filter(email=email).count()
            if users > 0 :
                messages.error(request, "Email Already Registered")
                return redirect('home')

            user = User(username=username, email=email, first_name=fname, last_name=lname, organization=org,
                        country=country,Region=region, webpage=page, Role=usertype, Topic=topic)
            user.set_password(password)
            User.save(user)
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
    return render(request, 'signup.html')


def handle_login(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
        try:
            user = authenticate(email=email, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "welcome:{}".format(request.user))
                return redirect('home')
        except Exception as E:
            messages.error(request, "No such a user Exists")
        messages.error(request, "Wrong Email or Password")
    return render(request, 'login.html')


def home(request):
    if request.user.is_authenticated:
        role = request.user.Role
        data = {'U': request.user,'role':role}
        if role == "Chair":
            return render(request, 'dashboard.html', data)
        elif role == "Author":
            return render(request, 'dashboard_author.html', data)
        else:
            return render(request, 'dashboard_reviewer.html', data)
    return render(request, 'home.html')


def registrationtext(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        subject = 'Reset Password'
        to = email
        random1 = random.randint(9999, 999999)
        random2 = random.randint(9999, 999999)
        Domain = get_current_site(request).domain
        html_message = render_to_string('RegsitertxtConfirmEmail.html', {'Domain': Domain,
                                                                         'key1': random1, 'key2': random2,
                                                                         'email': email})
        plain_message = strip_tags(html_message)
        try:
            RegisterEmailTxt.objects.get(email=email).delete()
        except:
            pass
        keys = RegisterEmailTxt(email=email, key1=random1, key2=random2)
        keys.save()
        mail.send_mail(subject, plain_message, EMAIL_HOST_USER, [to], html_message=html_message)
        messages.error(request,'WE have sent an activation link on your email please click to proceed Further')
        return render(request, 'registration.html')
    return render(request, 'registration.html')


def ConfirmRegisterTXT(request, email, random1, random2):
# def ConfirmRegisterTXT(request):
    Check = RegisterEmailTxt.objects.get(email=email,key1=random1, key2=random2)
    if Check:
        Check.delete()
        return render(request, 'RegistrationConfirmed.html')
    messages.error(request, 'Invalid Link')
    return redirect('home')


def overview(request):
    return render(request, 'overview.html')


def policy(request):
    return render(request, 'policy.html')


def privacy(request):
    return render(request, 'privacy.html')


def contact_us(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        msg = request.POST.get('message')

        update = Contact(name=name)
        update.email = email
        update.subject = subject
        update.msg = msg
        update.save()

        if update:
            send_mail(
                subject,
                "Name: {} email: {} , message: {}".format(name, email, msg),
                '',
                ['']
            )
    return render(request, 'contact.html')


def feedback(request):
    name = request.POST.get('name')
    email = request.POST.get('email')
    feedback = request.POST.get('feedback')
    update = Feedback(name=name)
    update.email = email
    update.feedback = feedback
    update.save()

    if update:
        send_mail(
            "FEEDBACK",
            "Name: {} email: {} , feedback: {}".format(name, email, feedback),
            '',
            ['']
        )
    return render(request, 'feedback.html')


def conference(request):
    return render(request, 'conference.html')

def handle_logout(request):
    logout(request)
    try:
        request.session['user'].delete()
    except:
        pass
    return redirect('login')


def forget_password(request):
    if request.method == 'POST':
        email = request.POST['email']
        check_email_exists = User.objects.filter(email=email)
        if check_email_exists.exists():
            subject = 'Reset Password'
            to = email
            html_message = render_to_string('password_reset_email.html', {'context': 'values'})
            plain_message = strip_tags(html_message)
            mail.send_mail(subject, plain_message, EMAIL_HOST_USER, [to], html_message=html_message)
            return render(request, 'password_reset_sent.html')
        else:
            messages.error(request, "User Not Exist registered")
            return redirect('home')
