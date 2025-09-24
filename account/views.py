from django.shortcuts import render,redirect
from account.forms import RegistrationForm 
from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib import messages
from django.conf import settings
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.urls import reverse
from account.utils import send_activation_email, send_reset_password_email
from core.models import User
from django.contrib.auth import authenticate, login

def home(request):
    return render(request, 'account/home.html')


def register_view(request):
    if request.method == 'POST':
        form = RegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_active = False
            user.save()
            uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
            token = default_token_generator.make_token(user)
            relative_link = reverse('activate', kwargs={'uidb64': uidb64,'token': token})
            activation_link = f"{settings.SITE_DOMAIN.rstrip('/')}{relative_link}"
            send_activation_email(user.email, activation_link)
            messages.success(request, 'Registration successful! Check your email to activate your account.')
            return redirect('login')
    else:
        form = RegistrationForm()
    return render(request, 'account/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        if request.user.is_seller:
            return redirect('seller_dashboard')
        elif request.user.is_customer:
            return redirect('customer_dashboard')
        return redirect('home')
    if request.method=='POST':
        email=request.POST.get('email')
        password=request.POST.get('password')
        if not email or not password:
            messages.error(request, 'Both fields are required.')
            return redirect('login')
        try:
            user=User.objects.get(email=email)
        except User.DoesNotExist:
            messages.error(request, 'Invalid email or password')
            return redirect('login')
        if not user.is_active:
            messages.error(
                request, 'Your account is inactive. Please activate your account'
            )
            return redirect('login')
        user=authenticate(request, email=email, password=password)
        if user is not None:
            login(request, user)
    return render(request, 'account/login.html')


def activate_account(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except Exception:
        user = None
    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Account activated successfully.')
        return redirect('login')
    else:
        messages.error(request, 'Activation link is invalid or expired.')
        return redirect('register')


def password_reset_view(request):
    if request.method=='POST':
        form=PasswordResetForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data.get('email')
            user=User.objects.filter(email=email).first()
            if user:
                uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
                token = default_token_generator.make_token(user)
                reset_url=reverse('password_reset_confirm', kwargs={'uidb64': uidb64, 'token': token})
                absolute_reset_url=f'{request.build_absolute_uri(reset_url)}'
                send_reset_password_email(user.email, absolute_reset_url)
                messages.success(request, ('We have sent you a password reset link. Please check your email'))
                return redirect('login')
        else:
            form=PasswordResetForm()
    return render(request, 'account/password_reset.html')


def password_reset_confirm_view(request, uidb64, token):
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=uid)
        if not default_token_generator.check_token(user, token):
            messages.error(request, ('This link has expired or is invalid'))
            return redirect('password_reset')
        if request.method=='POST':
            form=SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,('Your password has been successful reset'))
                return redirect('login')
            else:
                for field, errors in form.errors.items():
                    for error in errors:
                        messages.error(request, error)
        else:
            form=SetPasswordForm(user)
        return render(request, 'account/password_reset_confirm.html', {'form':form, 'uidb64':uidb64, 'token':token})
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        messages.error(request,('An error occurred. Please try again later.'))
        return redirect('password_reset')
