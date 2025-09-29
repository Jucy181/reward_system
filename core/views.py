from django.contrib import messages
from django.contrib.auth import logout, get_user_model
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import serializers, generics, status
from rest_framework import viewsets, permissions
from rest_framework.views import APIView

from .forms import SubmissionForm
from .models import App, Submission, UserProfile, AndroidApp, TaskCompleted
from .serializers import AppSerializer, SubmissionSerializer, UserProfileSerializer, UserSerializer, \
    TaskCompletedSerializer, TaskScreenshotSerializer
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from .serializers import SignupSerializer

User = get_user_model()


# Create your views here.
@api_view(['GET'])
def test_api(request):
    return Response({"message": "DRF is working!"})


class AppViewSet(viewsets.ModelViewSet):
    queryset = App.objects.filter(status='approved')
    serializer_class = AppSerializer


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer


def home(request):
    return render(request, "core/home.html")


def profile(request):
    profile = UserProfile.objects.get(user=request.user)
    return render(request, "profile.html", {"profile": profile})


@login_required
def profile_view(request):
    profile = request.user.userprofile
    return render(request, "profile.html", {"profile": profile})


def logout_user(request):
    logout(request)
    return redirect('home')


@login_required
def submit_screenshot(request):
    if request.method == 'POST':
        form = SubmissionForm(request.POST, request.FILES)
        if form.is_valid():
            submission = form.save(commit=False)
            submission.user = request.user
            submission.approved = False
            submission.save()
            messages.success(request, "Screenshot submitted successfully")
            return redirect('core:home')
    else:
        form = SubmissionForm()
        return render(request, 'core/submit_screenshot.html', {'form': form})


class UserListView(generics.ListAPIView):
    queryset = User.objects.all().order_by('date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]


class UserProfileView(generics.RetrieveAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user.userprofile


class TaskCompleteView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        app_id = request.data.get('app_id')
        screenshot = request.FILES.get('screenshot')

        if not app_id or not screenshot:
            return Response({'error': 'app_id and screenshot are required'}, status=400)

        app = AndroidApp.objects.get(user=request.user)
        task = TaskCompleted.objects.create(user=request.user, app=app, screenshot=screenshot)

        profile = UserProfile.objects.get(user=request.user)
        profile.total_points += app.points
        profile.save()

        serializer = TaskCompletedSerializer(task)
        return Response(serializer.data)


def upload_screenshot(request):
    return render(request, "core/upload_screenshot.html")


class UploadScreenshotView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        serializer = TaskScreenshotSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
