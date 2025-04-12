from rest_framework import viewsets, status, generics
from rest_framework.decorators import action, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated, IsAdminUser
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenObtainPairView
from django.contrib.auth import get_user_model
from django.db.models import Q
from .serializers import (
    UserSerializers, 
    CustomTokenObtainPairSerializer,
    RegistrationSerializers,
    PasswordChangeSerializer
)
from .permissions import IsOwnerOrAdmin
from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample
from drf_spectacular.types import OpenApiTypes
from django.contrib.auth.tokens import default_token_generator


User = get_user_model()

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer

    @extend_schema(
        tags=['Authentication'],
        description='Login endpoint to obtain JWT tokens',
        responses={
            200: {
                'description': 'Successfully authenticated',
                'examples': [{
                    'access': 'string',
                    'refresh': 'string',
                    'user': {
                        'id': 'uuid',
                        'email': 'user@example.com',
                        'first_name': 'John',
                        'last_name': 'Doe',
                        'role': 'attendant'
                    }
                }]
            }
        }
    )
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)

class UserView(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializers
    permission_classes = [IsAuthenticated, IsOwnerOrAdmin]

    def get_queryset(self):
        queryset = User.objects.all()
        if self.request.user.role != 'admin' and self.request.user.role != 'administrator':
            return User.objects.filter(id=self.request.user.id)
        
        # Search functionality
        search = self.request.query_params.get('search', None)
        role = self.request.query_params.get('role', None)
        
        if search:
            queryset = queryset.filter(
                Q(first_name__icontains=search) |
                Q(last_name__icontains=search) |
                Q(email__icontains=search)
            )
        
        if role:
            queryset = queryset.filter(role=role)
            
        return queryset
    
    @extend_schema(
        tags=['Users'],
        description='Get list of users (admin only)',
        parameters=[
            OpenApiParameter('role', OpenApiTypes.STR, enum=['attendant', 'admin', 'administrator']),
            OpenApiParameter('search', OpenApiTypes.STR, description='Search by name or email'),
        ]
    )
    def list(self, request, *args, **kwargs):
        return super().list(request, *args, **kwargs)
    
    @extend_schema(
        tags=['Users'],
        description='Get or update current user profile'
    )
    @action(detail=False, methods=['get', 'patch'])
    def me(self, request):
        if request.method == 'GET':
            serializer = self.get_serializer(request.user)
            return Response(serializer.data)
        elif request.method == 'PATCH':
            serializer = self.get_serializer(request.user, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    @extend_schema(
        tags=['Users'],
        description='Change user password',
        request=PasswordChangeSerializer
    )
    @action(detail=False, methods=['post'])
    def change_password(self, request):
        serializer = PasswordChangeSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            
        user = request.user
        if not user.check_password(serializer.validated_data['old_password']):
            return Response(
                {'old_password': 'Wrong password.'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        user.set_password(serializer.validated_data['new_password'])
        user.save()
        return Response({'message': 'Password updated successfully'})

    @extend_schema(
        tags=['Users'],
        description='Initiate password reset process',
        request={'application/json': {'type': 'object', 'properties': {'email': {'type': 'string'}}}}
    )
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def forgot_password(self, request):
        email = request.data.get('email')
        if not email:
            return Response(
                {'error': 'Email is required'},
                status=status.HTTP_400_BAD_REQUEST
            )
            
        try:
            user = User.objects.get(email=email)
            token = default_token_generator.make_token(user)
            # TODO: Send password reset email with token
            return Response({'message': 'Password reset email sent'})
        except User.DoesNotExist:
            return Response(
                {'error': 'No user found with this email address'},
                status=status.HTTP_404_NOT_FOUND
            )


class RegistrationView(viewsets.ModelViewSet):
    authentication_classes = []  
    permission_classes = [AllowAny]
    queryset = User.objects.none()  # Don't expose user list to unauthenticated users
    serializer_class = RegistrationSerializers
    http_method_names = ['post']  # Only allow POST method

    @extend_schema(
        tags=['Authentication'],
        description='Register a new user account',
        request=RegistrationSerializers,
        responses={
            201: UserSerializers,
            400: {'description': 'Bad Request - Invalid data provided'}
        }
    )
    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        user = serializer.save()
        return Response(
            UserSerializers(user).data,
            status=status.HTTP_201_CREATED
        )