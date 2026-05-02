from rest_framework import viewsets, permissions
from .models import Subject, Topic
from .serializers import SubjectSerializer, TopicSerializer


class SubjectViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Subject.objects.prefetch_related('topics').all()
    serializer_class = SubjectSerializer
    permission_classes = [permissions.IsAuthenticated]


class TopicViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Topic.objects.select_related('subject').all()
    serializer_class = TopicSerializer
    permission_classes = [permissions.IsAuthenticated]
