from users.models import CustomUser
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken

User = get_user_model()

class LoginSerializer(serializers.Serializer):
    email=serializers.EmailField(required=True)
    password=serializers.CharField(write_only=True,required=True)

    def validate(self,attrs):
        email=attrs.get("email")
        password=attrs.get("password")

        if email and password:
            user = authenticate(request=self.context.get('request'),email=email,password=password)

            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User is disabled")
            else:
                raise serializers.ValidationError("Unable to login with given credentials")
        else:
            raise serializers.ValidationError("must include email and password")

        attrs['user']=user
        return attrs
    


class SignUpSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True, validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password2', 'phone', 'owner', 'name')
        extra_kwargs = {
            'phone': {'required': True}
        }
    
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        return attrs

    def create(self, validated_data):
        user = User.objects.create(
            email=validated_data['email'],
            phone=validated_data['phone'],
            # name=validated_data['name'],
            owner=validated_data['owner'] 
        )
    
        user.set_password(validated_data['password'])
        user.save()

        return user


# Need to perform other actions to get it
class TokenSerializer(serializers.Serializer):
    token=serializers.CharField(read_only=True)

    def validate(self, attrs):
        user=self.context['request'].user
        if not user or not user.is_authenticated:
            raise serializers.ValidationError("User is not authenticated")
        refresh=RefreshToken.for_user(user)
        attrs['token']={
            'refresh':str(refresh),
            'access':str(refresh.access_token)
        }
        return attrs