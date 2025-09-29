from django.contrib.auth.models import User
from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

# Create your models here.
STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('approved', 'Approved'),

]


class App(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='apps', blank=True, null=True)
    points = models.PositiveIntegerField()
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')

    def __str__(self):
        return self.name


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_points = models.PositiveIntegerField(default=0)

    @property
    def tasks_completed(self):
        return TaskCompleted.objects.filter(user=self.user).count()

    def __str__(self):
        return self.user.username


class Submission(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app = models.ForeignKey(App, on_delete=models.CASCADE)
    screenshot = models.ImageField(upload_to='screenshots/')
    submitted_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}-{self.app.name}"


class AndroidApp(models.Model):
    name = models.CharField(max_length=255)
    points = models.PositiveIntegerField(default=0)


class TaskCompleted(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app = models.ForeignKey(AndroidApp, on_delete=models.CASCADE)
    screenshot = models.ImageField(upload_to='screenshots/')
    completed_at = models.DateTimeField(auto_now_add=True)


class TaskScreenshot(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    app_name = models.CharField(max_length=255)  # Or link to your App model if exists
    screenshot = models.ImageField(upload_to='screenshots/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.user.username} - {self.app_name}"
