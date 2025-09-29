from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_POST

from .forms import AppForm
from core.models import App, Submission, UserProfile

staff_required = user_passes_test(lambda u: u.is_staff, login_url='admin_panel:login')


# Create your views here.
def dashboard(request):
    apps = App.objects.all().order_by('created_at')
    return render(request, 'admin_panel/dashboard.html')


def add_app(request):
    if request.method == 'POST':
        form = AppForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:dashboard')
    else:
        form = AppForm()
    return render(request, 'admin_panel/add_app.html', {'form': form})


def admin_app_list(request):
    apps = App.objects.all()
    return render(request, 'admin_panel/admin_app_list.html', {'apps': apps})


def edit_app(request, app_id):
    app = get_object_or_404(App, id=app_id)
    if request.method == 'POST':
        form = AppForm(request.POST, request.FILES, instance=app)
        if form.is_valid():
            form.save()
            return redirect('admin_panel:admin_app_list')

    else:
        form = AppForm(instance=app)
    return render(request, 'admin_panel/edit_app.html', {'form': form, 'app': app})


def delete_app(request, app_id):
    app = get_object_or_404(App, id=app_id)
    if request.method == 'POST':
        app.delete()
        return redirect('admin_panel:admin_app_list')
    return render(request, 'admin_panel/delete_app.html', {'app': app})


def submissions_list(request):
    submissions = Submission.objects.all().order_by('-submitted_at')
    return render(request, 'admin_panel/submissions_list.html', {'submissions': submissions})


def approve_submission(request, sub_id):
    sub = get_object_or_404(Submission, id=sub_id)
    if not sub.approved:
        sub.approved = True
        sub.save()
        profile, created = UserProfile.objects.get_or_create(user=sub.user)
        profile.total_points += sub.app.points
        profile.save()
        return redirect('admin_panel:submissions_list')


def reject_submission(request, sub_id):
    sub = get_object_or_404(Submission, id=sub_id)
    if not sub.approved:
        sub.delete()
        return redirect('admin_panel:submissions_list')


@staff_required
def dashboard(request):
    pending = Submission.objects.filter(approved=False).select_related('user', 'app').order_by('-submitted_at')
    approved = Submission.objects.filter(approved=True).select_related('user', 'app').order_by('-submitted_at')
    return render(request, 'admin_panel/dashboard.html', {'pending': pending, 'approved': approved})


@staff_required
@require_POST
def approve_submission(request, pk):
    if request.method != 'POST':
        return redirect('admin_panel:dashboard')

    sub = get_object_or_404(Submission, pk=pk)
    if sub.approved:
        messages.info(request, "Submission already approved.")
        return redirect('admin_panel:dashboard')

    sub.approved = True
    sub.save()

    profile, created = UserProfile.objects.get_or_create(user=sub.user)
    profile.total_points += sub.app.points
    profile.save()

    messages.success(request, f"Approved submission and added {sub.app.points} points to {sub.user.username}.")
    return redirect('admin_panel:dashboard')


@staff_required
@require_POST
def reject_submission(request, pk):
    if request.method != 'POST':
        return redirect('admin_panel:dashboard')

    sub = get_object_or_404(Submission, pk=pk)
    sub.delete()
    messages.success(request, "Submission rejected ans deleted.")
    return redirect('admin_panel:dashboard')


def admin_login(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None and user.is_staff:
            login(request, user)
            return redirect('admin_panel:dashboard')
        else:
            messages.error(request, "Invalid credentials or not staff ")
    return render(request, 'admin_panel/login.html')
