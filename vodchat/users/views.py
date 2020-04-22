from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound, HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_text
from .token import account_activation_token
from django.core.mail import EmailMultiAlternatives, send_mail
from . import forms

@login_required(login_url='/login')
def index(request):
  # if not request.user.is_authenticated:
  #   return HttpResponseRedirect(reverse('login'))
  return HttpResponseRedirect(reverse('videos'))

def signup(request):
    context = {}
    if request.method == 'POST':
        form = forms.SignupForm(request.POST)
        if form.is_valid():
            try:
                user = User.objects.create_user(
                    form.cleaned_data['username'], 
                    email=form.cleaned_data['email'], 
                    password=form.cleaned_data['password'])
                user.is_active = False
                current_site = get_current_site(request)
                mail_subject = "Activate your account"
                token = account_activation_token.make_token(user)
                send_mail(mail_subject, f"Click to activate your accont: http://{current_site.domain}{reverse('activate', kwargs={'uid': user.id, 'token': token})}", 'leyao.zhang@mail.mcgill.ca', [f'{user.email}'])
                # message = EmailMultiAlternatives(
                #     subject=mail_subject,
                #     body=f"Click to activate your accont: http://{current_site.domain}{reverse('activate', kwargs={'uidb64': uid, 'token': token})}",
                #     from_email='Lily leyao.zhang@mail.mcgill.ca',
                #     to=[f'{user.username} {user.email}']
                # )
                # message.send()
                return HttpResponse('Verification Email sent.')
            except IntegrityError:
                form.add_error('username', 'Username is taken')

        context['form'] = form   
    return render(request, 'users/signup.html', context)

def activate(request, uid, token):
    try:
        user = User.objects.get(id=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        return render(request, 'users/activate_success.html')
    return HttpResponse('Invalid activation link')


def do_login(request):
    context = {}
    if request.method == 'POST':
        form = forms.LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request, 
              username=form.cleaned_data['username'], 
              password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                if 'next' in request.GET:
                    return HttpResponseRedirect(request.GET['next'])
                return HttpResponseRedirect(reverse('videos'))
            else:
                form.add_error(None, 'Unable to log in')
        context['form'] = form
    return render(request, 'users/login.html', context)

def do_logout(request):
    logout(request)
    return HttpResponseRedirect(reverse('login'))
    
