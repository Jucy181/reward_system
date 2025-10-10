from django.contrib import messages
from django.forms import models
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from core.models import UserProfile
from core.models import Submission,App
from django.db.models import Sum
from django.views.decorators.http import require_POST


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
    return render(request, 'user_panel/profile.html', {'profile': profile})


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


@login_required
def user_submissions(request):
    submissions = Submission.objects.filter(user=request.user).order_by('-submitted_at')

    total_points = submissions.filter(approved=True).aggregate(total=Sum('app__points'))['total'] or 0

    return render(request, 'user_panel/user_submissions.html', {
        'submissions': submissions,
        'total_points': total_points
    })


@login_required
def user_dashboard(request):
    total_points = Submission.objects.filter(user=request.user, approved=True).aggregate(
        total=Sum('app__points')
    )['total'] or 0

    return render(request, 'user_panel/dashboard.html', {'total_points': total_points})


@login_required
def submit_screenshot(request):
    app = App.objects.first()

    if request.method == "POST":
        # Loop through all uploaded files
        for file in request.FILES.getlist('screenshot'):
            Submission.objects.create(user=request.user, app=app, screenshot=file)

        # Redirect to same page after successful upload
        return redirect('users:submit_screenshot')

    # Fetch all submissions by this user for display
    submissions = Submission.objects.filter(user=request.user).order_by('-submitted_at')

    return render(request, 'user_panel/submit_screenshot.html', {
        'submissions': submissions,
        'app': app,
    })


def custom_logout(request):
    logout(request)
    return redirect('users:login')
