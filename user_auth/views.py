from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth import authenticate, get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.exceptions import ValidationError
from .serializers import RegisterUserSerializer, LoginUserSerializer
from organisation.models import Organisation


User = get_user_model()

# Register user view
class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = RegisterUserSerializer
    
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            org_name = f'{user.first_name}\'s organisation'
            org = Organisation.objects.create(name=org_name)
            refresh = RefreshToken.for_user(user)
            return Response({
                'status': 'success',
                'message': 'Registration successful',
                'data': {
                    'accessToken': str(refresh.access_token),
                    'user': {
                        'user_id': user.id,
                        'first_name': user.first_name,
                        'last_name': user.last_name,
                        'email': user.email,
                        'phone': user.phone,
                    }
                },
            }, status=status.HTTP_201_CREATED)
        return Response({
            'status': 'Bad request',
            'message': 'Registration unsaccessful',
            'statusCode': status.HTTP_400_BAD_REQUEST
        }, status=status.HTTP_400_BAD_REQUEST)
    
# Login user view
class LoginUserView(generics.GenericAPIView):
    serializer_class = LoginUserSerializer
    
    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            password=serializer.validated_data['password']
            user = authenticate(request, email=email, password=password)
            if user is not None:
                refresh = RefreshToken.for_user(user)
                return Response({
                    'status': 'success',
                    'message': 'Login successful',
                    'data': {
                        'accessToken': str(refresh.access_token),
                        'user': {
                            'user_id': user.id,
                            'first_name': user.first_name,
                            'last_name': user.last_name,
                            'email': user.email,
                            'phone': user.phone,
                        }
                    },
                }, status=status.HTTP_200_OK)
            else:
                return Response({
                    'status': 'Bad request',
                    'message': 'Authentication unsuccessful',
                    'statusCode': status.HTTP_401_UNAUTHORIZED
                }, status=status.HTTP_401_UNAUTHORIZED)
        return Response({
            'status': 'Bad request',
            'message': 'Login unsuccessful',
            'statusCode': '400'
        }, status=status.HTTP_401_UNAUTHORIZED)