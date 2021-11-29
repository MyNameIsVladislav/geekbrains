from django.contrib import admin

from feedback.models import FeedBack


@admin.register(FeedBack)
class FeedBackAdmin(admin.ModelAdmin):
    list_display = ['id', 'email', 'first_name', 'last_name', "status_request"]
    list_display_links = ('id',)
    list_filter = ['status_request', 'created_at']
    search_fields = ['first_name', 'last_name', 'email']
    ordering = ['first_name', 'last_name']
