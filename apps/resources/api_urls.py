from django.urls import path
from .api_views import ResourceListView

urlpatterns = [
    path('topic/<int:topic_id>/', ResourceListView.as_view(), name='resource-list'),
]
