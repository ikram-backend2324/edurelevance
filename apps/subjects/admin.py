from django.contrib import admin
from .models import Subject, Topic


class TopicInline(admin.TabularInline):
    model = Topic
    extra = 1
    fields = ['name', 'description']

    def save_model(self, request, obj, form, change):
        obj.is_public = True
        obj.created_by = None
        super().save_model(request, obj, form, change)


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ['name', 'topic_count', 'is_public', 'created_by', 'created_at']
    search_fields = ['name']
    inlines = [TopicInline]
    list_per_page = 20

    def save_model(self, request, obj, form, change):
        obj.is_public = True
        obj.created_by = None
        super().save_model(request, obj, form, change)


@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
    list_display = ['name', 'subject', 'is_public', 'created_by', 'resource_count', 'created_at']
    list_filter = ['subject', 'is_public']
    search_fields = ['name', 'subject__name']
    list_per_page = 20

    def save_model(self, request, obj, form, change):
        obj.is_public = True
        obj.created_by = None
        super().save_model(request, obj, form, change)