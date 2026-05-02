from django.urls import path
from . import views

app_name = 'subjects'

urlpatterns = [
    path('', views.subject_list, name='list'),
    path('<int:pk>/', views.subject_detail, name='detail'),
    path('topic/<int:pk>/', views.topic_detail, name='topic_detail'),
    path('create/', views.create_subject, name='create_subject'),
    path('<int:subject_pk>/create-topic/', views.create_topic, name='create_topic'),
]