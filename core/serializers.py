from rest_framework import serializers
from django.contrib.auth.models import User
from .models import App, Submission, UserProfile, TaskCompleted, TaskScreenshot


class AppSerializer(serializers.ModelSerializer):
    class Meta:
        model = App
        fields = '__all__'


class SubmissionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Submission
        fields = '__all__'


class UserProfileSerializer(serializers.ModelSerializer):
    tasks_completed = serializers.IntegerField(read_only=True)

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
        read_only_fields = ['user', 'uploaded_at']

    def validate_screenshot(self, value):
        if not value.name.lower().endswith(('.png', '.jpg', '.jpeg')):
            raise serializers.ValidationError("Only PNG/JPG images are allowed.")
        return value

    def create(self, validated_data):
        request = self.context.get('request', None)
        user = getattr(request, 'user', None)
        if user is None:
            user = User.objects.first()
        return TaskScreenshot.objects.create(user=user, **validated_data)


class ScreenshotSerializer(serializers.ModelSerializer):
    class Meta:
        model = TaskScreenshot
        fields = ['app_name', 'screenshot', 'uploaded_at']
        read_only_fields = ['uploaded_at']

    def create(self, validated_data):
        request = self.context.get('request', None)
        user = getattr(request, 'user', None)
        if not user or not user.is_authenticated:
            user = User.objects.first()

        return TaskScreenshot.objects.create(user=user, **validated_data)
