from rest_framework import viewsets
from .serializer import *
from users.models import *
from rest_framework.response import Response
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

User=get_user_model()

class SignupModelViewSet(viewsets.ModelViewSet):
    queryset=User.objects.all()
    serializer_class=SignUpSerializer
    
    def get_queryset(self):
        return None

class LoginModelViewSet(viewsets.ViewSet):
    serializer_class = LoginSerializer
    queryset=User.objects.all()

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            refresh=RefreshToken.for_user(user)
            response = {
                'user': f'{user.email} is logged in',
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }
            return Response(response)

        return Response({'errors': serializer.errors})