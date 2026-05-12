from django.contrib import admin
from .models import AIEvaluation


@admin.register(AIEvaluation)
class AIEvaluationAdmin(admin.ModelAdmin):
    list_display = ['user', 'subject_name', 'topic_name', 'score_percent', 'label', 'language', 'created_at']
    list_filter = ['label', 'language', 'resource_type', 'created_at']
    search_fields = ['user__username', 'subject_name', 'topic_name', 'resource_title']
    readonly_fields = ['score', 'label', 'reason', 'key_matches', 'missing_topics', 'raw_text', 'created_at']
    list_per_page = 25
    date_hierarchy = 'created_at'

    fieldsets = (
        ('User & Input', {
            'fields': ('user', 'subject_name', 'topic_name', 'topic_description', 'language')
        }),
        ('Resource', {
            'fields': ('resource_type', 'resource_title', 'resource_url', 'resource_text', 'raw_text')
        }),
        ('AI Result', {
            'fields': ('score', 'label', 'reason', 'key_matches', 'missing_topics')
        }),
        ('Meta', {
            'fields': ('created_at',)
        }),
    )