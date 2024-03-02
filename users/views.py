# users/views.py
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect

from sensors_api.models import UserDashboard
from .forms import UserRegisterForm, UserLoginForm
from django.contrib.auth.decorators import login_required


@login_required(login_url='/login/')
def home(request):
    dashboard_link = UserDashboard.objects.get(user=request.user).dashboard_link
    return render(request, 'index.html', {
        "dashboard_link": dashboard_link,
    })


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()  # Save the user
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(request, email=email, password=password)  # Authenticate the user
            if user is not None:
                login(request, user)  # Log in the user
                return redirect('home')  # Redirect to home or any other page after login
    else:
        form = UserRegisterForm()
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            # Instead of accessing 'email', use 'username' as it corresponds to the user's email
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to home or any other page after login
        # If form is not valid, render the login form again with errors
        return render(request, 'users/login.html', {'form': form})
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
    return redirect('login')
