from django.contrib import admin
from .models import Resource, RelevanceScore


class RelevanceScoreInline(admin.StackedInline):
    model = RelevanceScore
    readonly_fields = ['score', 'label', 'reason', 'key_matches', 'missing_topics', 'evaluated_at']
    can_delete = False
    extra = 0


@admin.register(Resource)
class ResourceAdmin(admin.ModelAdmin):
    list_display = ['title', 'topic', 'resource_type', 'uploaded_by', 'is_evaluated', 'uploaded_at']
    list_filter = ['resource_type', 'is_evaluated', 'topic__subject']
    search_fields = ['title', 'topic__name']
    readonly_fields = ['raw_text', 'is_evaluated', 'uploaded_at']
    inlines = [RelevanceScoreInline]
    list_per_page = 20


@admin.register(RelevanceScore)
class RelevanceScoreAdmin(admin.ModelAdmin):
    list_display = ['resource', 'topic', 'score', 'label', 'evaluated_at']
    list_filter = ['label', 'topic__subject']
    search_fields = ['resource__title']
    readonly_fields = ['evaluated_at']
    list_per_page = 20
