from django.contrib import admin
from django.utils.html import format_html

from .models import App, Submission, UserProfile


# Register your models here.
@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ('user', 'app', 'approved', 'submitted_at')
    list_filter = ('approved', 'submitted_at')


@admin.register(App)
class AppAdmin(admin.ModelAdmin):
    list_display = ('name', 'status', 'points', 'image_tag')

    def image_tag(self, obj):
        if obj.image:
            return format_html('<img src="{}" width ="50" height="50"/>'.format(obj.image.url))
        return "_"

    image_tag.short_description = 'Image'


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'total_points')
