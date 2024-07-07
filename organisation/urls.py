from django.urls import path
from .views import UserDetailView, OrganisationListView, OrganisationDetailsView, AddUserToOrganisationView


urlpatterns = [
    path('user/<str:pk>/', UserDetailView.as_view(), name='user-detail'),
    path('organisations/', OrganisationListView.as_view(), name='organisations_list'),
    path('organisations/<str:pk>/', OrganisationDetailsView.as_view(), name='organisation_details'),
    path('organisations/<str:pk>/users/', AddUserToOrganisationView.as_view(), name='organisation_add_user'),
]