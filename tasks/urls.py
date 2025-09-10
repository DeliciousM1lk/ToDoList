
from django.urls import path,include
from .views import *

app_name = 'tasks'

urlpatterns = [
    path('signup/',SignUpView.as_view(),name='signup'),
    path('',TaskListView.as_view(),name='list'),
    path('create/',TaskCreateView.as_view(),name='create'),
    path('<int:pk>/edit/',TaskUpdateView.as_view(),name='edit'),
    path('<int:pk>/', TaskDetailView.as_view(), name='detail'),
    path('<int:pk>/delete/',TaskDeleteView.as_view(),name='delete'),
]
