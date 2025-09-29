from rest_framework.routers import DefaultRouter
from django.urls import path, include
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import AppViewSet, SubmissionViewSet, test_api, UserListView, SignupView, UserProfileView, TaskCompleteView, \
    UploadScreenshotView
from . import views

router = DefaultRouter()
router.register(r'apps', AppViewSet)
router.register(r'submissions', SubmissionViewSet)

app_name = "core"

urlpatterns = [
    path('test/', test_api, name='test-api'),
    path('logout/', views.logout_user, name='logout'),
    path("", views.home, name="home"),
    path('profile-page/', views.profile_view, name='profile'),
    path('submit/', views.submit_screenshot, name='submit_screenshot'),
    path('users/', UserListView.as_view(), name='user-list'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', SignupView.as_view(), name='signup'),
    path('profile/', UserProfileView.as_view(), name='user-profile'),
    path('task/complete',TaskCompleteView.as_view(),name='task_complete'),
    path('upload-screenshot/',  views.upload_screenshot, name='upload-screenshot'),
    path('upload-screenshot/', UploadScreenshotView.as_view(), name='upload-screenshot'),

    path('', include(router.urls)),
]
