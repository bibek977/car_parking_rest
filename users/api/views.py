from rest_framework import viewsets
from .serializer import *
from users.models import *
from rest_framework.response import Response
from django.contrib.auth import get_user_model

User=get_user_model()

class SignupModelViewSet(viewsets.ModelViewSet):
    ...

class LoginModelViewSet(viewsets.ModelViewSet):
    ...