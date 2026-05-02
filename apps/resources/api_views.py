from rest_framework import generics, permissions
from .models import Resource
from .serializers import ResourceSerializer


class ResourceListView(generics.ListAPIView):
    serializer_class = ResourceSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        topic_id = self.kwargs['topic_id']
        return Resource.objects.filter(
            topic_id=topic_id
        ).select_related('score').order_by('-score__score')
