from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Organisation
from .serializers import OrganisationSerializer
# from user_auth.serializers import UserSerializer


User = get_user_model()

# Create your views here.
class UserDetailView(generics.RetrieveAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, pk):
        try:
            user = User.objects.get(id=pk)
            if user != request.user and user not in request.user.organisations.values_list('users', flat=True):
                return Response({
                    'status': 'Forbidden',
                    'message': 'You do not have access to this user\'s details',
                }, status=status.HTTP_403_FORBIDDEN)
            return Response({
                'status': 'success',
                'message': 'User details retrieved successfully',
                'data': {
                    'user_id': user.id,
                    'first_name': user.first_name,
                    'last_name': user.last_name,
                    'email': user.email,
                    'phone': user.phone,
                }
            }, status=status.HTTP_200_OK)
        except User.DoesNotExist:
            return Response({
                'status': 'Not found',
                'message': 'User not found',
            }, status=status.HTTP_404_NOT_FOUND)
        