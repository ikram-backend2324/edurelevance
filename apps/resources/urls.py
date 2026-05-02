from django.urls import path
from . import views

app_name = 'resources'

urlpatterns = [
    path('upload/', views.upload_resource, name='upload'),
    path('<int:pk>/', views.resource_detail, name='detail'),
    path('<int:pk>/delete/', views.delete_resource, name='delete'),
    path('<int:pk>/reevaluate/', views.reevaluate_resource, name='reevaluate'),
]
