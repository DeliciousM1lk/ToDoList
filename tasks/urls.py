
from django.urls import path,include
from .views import *

app_name = 'tasks'

urlpatterns = [
    path('signup/',SignUpView.as_view(),name='signup'),
]