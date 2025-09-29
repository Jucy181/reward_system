from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate
from core.models import UserProfile


# Create your views here.
def signup(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('profile')
    else:
        form = UserCreationForm()
    return render(request, 'users/signup.html', {'form': form})


@login_required
def profile(request):
    profile, _ = UserProfile.objects.get_or_create(user=request.user)
    return render(request, 'users/profile.html', {'profile': profile})


def user_login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('users:profile')
        else:
            messages.error(request, "Invalid username or password")
    else:
        form = AuthenticationForm()

    return render(request, 'users/login.html', {'form': form})
