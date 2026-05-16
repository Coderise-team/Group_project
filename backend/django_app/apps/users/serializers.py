from rest_framework import serializers
from .models import User


class UserRegisterSerializers(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ["id", "username", "password", "password2", "email", "avatar", "bio", "elo_rating"]
        extra_kwargs = {'password': {'write_only': True}}

    def validate_username(self, value):
        if User.object.filter(username=value).exists():
            raise serializers.ValidationError("This username already exists")
        return value

    def validate_email(self, value):
        if User.object.filter(email=value).exists():
            raise serializers.ValidationError("This email already exists")
        return value

    def validate(self, data):
        if data["password"] != data["password2"]:
            raise serializers.ValidationError("Password is incorrect")
        return data

    def create(self, verified_data):
        verified_data.pop("password2")
        user = User.objects.create_user(**verified_data)
        return user
