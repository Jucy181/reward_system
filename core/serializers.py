from rest_framework import serializers
from django.contrib.auth.models import User
from .models import App, Submission, UserProfile, TaskCompleted
from .models import UserProfile
from .models import TaskScreenshot


class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = '__all__'


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    tasks_completed = serializers.IntegerField(source='tasks_completed', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['user', 'total_points', 'tasks_completed']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'date_joined', 'is_active']


class SignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        return user


class TaskCompletedSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskCompleted
        fields = ['id', 'app', 'screenshot', 'completed_at']


class TaskScreenshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskScreenshot
        fields = ['id', 'user', 'app_name', 'screenshot', 'uploaded_at']
