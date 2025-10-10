from django.urls import path
from . import views
from django.contrib.auth import views as auth_views

app_name = "users"

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('login/', auth_views.LoginView.as_view(template_name='users/login.html'), name='login'),
    path('profile/', views.profile, name='profile'),
    path('my-submissions/', views.user_submissions, name='user_submissions'),
    path('submit-screenshot/', views.submit_screenshot, name='submit_screenshot'),
    path('dashboard/', views.user_dashboard, name='dashboard'),
    path('logout/', views.custom_logout, name='logout'),
]
