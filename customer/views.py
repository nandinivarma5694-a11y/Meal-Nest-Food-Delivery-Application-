from django.shortcuts import render, redirect
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def customer_dashboard_view(request):
    return render(request, 'customer/dashboard.html')

def password_change_view(request):
    if request.method=='POST':
        form=PasswordChangeForm(user=request.user, data=request.POST)
        if form.is_valid():
            form.save()    
            logout(request)
            messages.success(
                request, 'Password changed successfully. please log in with your new password'
            )
            return redirect('login')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
    else:
        form=PasswordChangeForm(user=request.user)
    return render(request, 'customer/password_change.html', {'form':form})
