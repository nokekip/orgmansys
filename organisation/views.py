from django.contrib.auth import get_user_model
from rest_framework import generics, status, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Organisation
from .serializers import OrganisationSerializer
from rest_framework.views import APIView


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


class OrganisationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        organisations = Organisation.objects.filter(users=user)
        serializer = OrganisationSerializer(organisations, many=True)
        return Response({
            "status": "success",
            "message": "Organisations retrieved successfully",
            "data": {
                "organisations": [
                    {
                        "orgId": organisation['id'],
                        "name": organisation['name'],
                        "description": organisation['description']
                    }
                    for organisation in serializer.data
                ]
            }
        }, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = OrganisationSerializer(data=request.data)
        if serializer.is_valid():
            organisation = serializer.save()
            organisation.users.add(request.user)
            return Response({
                "status": "success",
                "message": "Organisation created successfully",
                "data": {
                    "orgId": str(organisation.id),
                    "name": organisation.name,
                    "description": organisation.description
                }
            }, status=status.HTTP_201_CREATED)
        return Response({
            "status": "Bad Request",
            "message": "Client error",
            "statusCode": 400,
            "errors": serializer.errors
        }, status=status.HTTP_400_BAD_REQUEST)

class OrganisationDetailsView(generics.RetrieveAPIView):
    queryset = Organisation.objects.all()
    serializer_class = OrganisationSerializer
    permission_classes = [permissions.IsAuthenticated]
    lookup_field = 'pk'

    def retrieve(self, request, *args, **kwargs):
        organisation = self.get_object()
        serializer = self.get_serializer(organisation)
        return Response({
            "status": "success",
            "message": "Organisation retrieved successfully",
            "data": {
                "orgId": serializer.data['id'],
                "name": serializer.data['name'],
                "description": serializer.data['description']
            }
        }, status=status.HTTP_200_OK)

class AddUserToOrganisationView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, *args, **kwargs):
        organisation_id = kwargs.get('pk')
        user_id = request.data.get('userId')

        if not user_id:
            return Response({
                "status": "Bad Request",
                "message": "User ID is required",
                "statusCode": 400
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            organisation = Organisation.objects.get(id=organisation_id)
            user = User.objects.get(id=user_id)
        except Organisation.DoesNotExist:
            return Response({
                "status": "Bad Request",
                "message": "Organisation not found",
                "statusCode": 400
            }, status=status.HTTP_400_BAD_REQUEST)
        except User.DoesNotExist:
            return Response({
                "status": "Bad Request",
                "message": "User not found",
                "statusCode": 400
            }, status=status.HTTP_400_BAD_REQUEST)

        organisation.users.add(user)
        organisation.save()

        return Response({
            "status": "success",
            "message": "User added to organisation successfully",
        }, status=status.HTTP_200_OK)
