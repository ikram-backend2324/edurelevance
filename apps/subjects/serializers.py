from rest_framework import serializers
from .models import Subject, Topic


class TopicSerializer(serializers.ModelSerializer):
    resource_count = serializers.SerializerMethodField()

    class Meta:
        model = Topic
        fields = ['id', 'name', 'description', 'resource_count', 'created_at']

    def get_resource_count(self, obj):
        return obj.resource_count()


class SubjectSerializer(serializers.ModelSerializer):
    topics = TopicSerializer(many=True, read_only=True)
    topic_count = serializers.SerializerMethodField()

    class Meta:
        model = Subject
        fields = ['id', 'name', 'description', 'topic_count', 'topics', 'created_at']

    def get_topic_count(self, obj):
        return obj.topic_count()
