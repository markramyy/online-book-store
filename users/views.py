from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required

from users.forms import LoginForm, UserCreationForm, EditProfileForm, ChangePasswordForm
from users.middleware import customer_required


def register_user(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            if user.is_customer:
                return redirect('customer_dashboard')
            elif user.is_admin:
                return redirect('admin_dashboard')
    else:
        form = UserCreationForm()
    return render(request, 'users/register_user.html', {'form': form})


def login_user(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            user = form.cleaned_data['user']
            login(request, user)
            if user.is_customer:
                return redirect('customer_dashboard')
            elif user.is_admin:
                return redirect('admin_dashboard')
    else:
        form = LoginForm()
    return render(request, 'users/login.html', {'form': form})


def logout_user(request):
    logout(request)
    return redirect('login')


@login_required
@customer_required
def edit_profile(request):
    if request.method == 'POST':
        form = EditProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('customer_dashboard')
    else:
        form = EditProfileForm(instance=request.user)
    return render(request, 'users/edit_profile.html', {'form': form})


@login_required
def change_password(request):
    if request.method == 'POST':
        form = ChangePasswordForm(request.POST)
        if form.is_valid():
            user = request.user
            if not user.check_password(form.cleaned_data['old_password']):
                form.add_error('old_password', 'Incorrect old password')
            else:
                user.set_password(form.cleaned_data['new_password'])
                user.save()
                return redirect('login')
    else:
        form = ChangePasswordForm()
    return render(request, 'users/change_password.html', {'form': form})
