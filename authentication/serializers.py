from django.contrib.auth.base_user import AbstractBaseUser
from rest_framework import serializers
from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

class RegistrationSerializer(serializers.ModelSerializer):

    password2 = serializers.CharField(style={"input_type": "password"}, write_only=True)

    class Meta:
        model = get_user_model()
        fields = ("username", "email", "password", "password2")
        extra_kwargs = {
            "password": {"write_only": True},
        }

    def validate (self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError({"password2": "Password fields didn't match."})
        return data
    
    def validate_password(self, value):
        # Use Django's built-in validators
        validate_password(value)
        return value

    def create(self, validated_data) -> AbstractBaseUser:
        user = get_user_model()(
            email=validated_data["email"], # type: ignore
            username=validated_data["username"], # type: ignore
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        style={"input_type": "password"}, write_only=True)


class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = get_user_model()
        fields = ("username", "email")
