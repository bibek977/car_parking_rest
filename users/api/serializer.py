from users.models import CustomUser
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    ...

class SignUpSerializer(serializers.ModelSerializer):
    ...