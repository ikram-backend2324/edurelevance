from django.urls import path
from rest_framework.routers import DefaultRouter
from .api_views import SubjectViewSet, TopicViewSet

router = DefaultRouter()
router.register('', SubjectViewSet, basename='subject')

urlpatterns = router.urls
