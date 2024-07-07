from django.urls import path
from .views import UserDetailView


urlpatterns = [
    path('user/<str:pk>/', UserDetailView.as_view(), name='user-detail'),
]