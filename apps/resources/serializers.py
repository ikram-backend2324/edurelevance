from rest_framework import serializers
from .models import Resource, RelevanceScore


class RelevanceScoreSerializer(serializers.ModelSerializer):
    score_percent = serializers.SerializerMethodField()

    class Meta:
        model = RelevanceScore
        fields = ['score', 'score_percent', 'label', 'reason', 'key_matches', 'missing_topics', 'evaluated_at']

    def get_score_percent(self, obj):
        return obj.score_percent()


class ResourceSerializer(serializers.ModelSerializer):
    score = RelevanceScoreSerializer(read_only=True)
    uploaded_by = serializers.StringRelatedField()

    class Meta:
        model = Resource
        fields = ['id', 'title', 'resource_type', 'url', 'is_evaluated', 'score', 'uploaded_by', 'uploaded_at']
