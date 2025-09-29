from django.urls import path
from . import views

app_name = "admin_panel"

urlpatterns = [
    path('', views.dashboard, name='custom_admin_dashboard'),
    path('add-app/', views.add_app, name='add_app'),
    path('apps/', views.admin_app_list, name='admin_app_list'),
    path('apps/edit/<int:app_id>/', views.edit_app, name='edit_app'),
    path('apps/delete/<int:app_id>/', views.delete_app, name='delete_app'),
    path('submissions/', views.submissions_list,name ='submissions_list'),
    path('submission/approve/<int:pk>/', views.approve_submission, name='approve_submission'),
    path('submissions/reject/<int:pk>/', views.reject_submission, name='reject_submission'),
    path('login/', views.admin_login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
