from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth import logout, get_user_model
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema

from rest_framework.decorators import api_view, permission_classes
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework import generics, permissions, status
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework_simplejwt.authentication import JWTAuthentication

from . import models
from .forms import SubmissionForm
from .models import App, Submission, UserProfile, TaskCompleted, TaskScreenshot
from .serializers import (
    AppSerializer,
    SubmissionSerializer,
    UserProfileSerializer,
    UserSerializer,
    SignupSerializer,
    TaskCompletedSerializer,
    TaskScreenshotSerializer, ScreenshotSerializer,
)

User = get_user_model()


# ------------------- API / Test -------------------
@api_view(['GET'])
def test_api(request):
    return Response({"message": "DRF is working!"})


# ------------------- ViewSets -------------------
class AppViewSet(viewsets.ModelViewSet):
    queryset = App.objects.filter(status='approved')
    serializer_class = AppSerializer
    permission_classes = [IsAdminUser]


class SubmissionViewSet(viewsets.ModelViewSet):
    queryset = Submission.objects.all()
    serializer_class = SubmissionSerializer
    permission_classes = [IsAdminUser]


class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer
    permission_classes = [IsAdminUser]


# ------------------- Template Views -------------------
def home(request):
    return render(request, "core/home.html")


@login_required
def profile_view(request):
    profile = request.user.userprofile
    return render(request, "profile.html", {"profile": profile})


@login_required
def upload_screenshot_page(request):
    return render(request, 'core/upload_screenshot.html')


def logout_user(request):
    logout(request)
    return redirect('home')


# ------------------- API Views -------------------
class UserListView(generics.ListAPIView):
    queryset = User.objects.all().order_by('date_joined')
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]


class SignupView(generics.CreateAPIView):
    serializer_class = SignupSerializer
    permission_classes = [permissions.AllowAny]


class UserProfileRetrieveView(generics.RetrieveAPIView):
    """
    Returns the profile of the currently logged-in user
    """
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

        try:
            app = App.objects.get(id=app_id)
        except App.DoesNotExist:
            return Response({'error': 'App not found'}, status=404)

        # Create task completed entry
        task = TaskCompleted.objects.create(user=request.user, app=app, screenshot=screenshot)

        # Update user profile points
        profile = UserProfile.objects.get(user=request.user)
        profile.total_points += app.points
        profile.save()

        serializer = TaskCompletedSerializer(task)
        return Response(serializer.data)


class UploadScreenshotView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        request_body=TaskScreenshotSerializer,
        responses={200: TaskScreenshotSerializer}
    )
    def post(self, request):
        serializer = TaskScreenshotSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response({
                "message": "Screenshot uploaded successfully!",
                "screenshot": serializer.data
            })
        return Response(serializer.errors, status=400)


class ScreenshotListView(generics.ListAPIView):
    serializer_class = ScreenshotSerializer
    permission_classes = [permissions.IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def get_queryset(self):
        return TaskScreenshot.objects.filter(user=self.request.user).order_by('uploaded_at')


@staff_member_required
def add_app_view(request):
    if request.method == 'POST':
        form = AppForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "App added successfully!")
            return redirect('admin_panel:add_app')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = AppForm()

    apps = App.objects.all()
    return render(request, 'admin_panel/add_app.html', {'form': form, 'apps': apps})


class AdminAppCreateAPIView(generics.CreateAPIView):
    queryset = App.objects.all()
    serializer_class = AppSerializer
    permission_classes = [permissions.IsAdminUser]
    parser_classes = [MultiPartParser, FormParser]
