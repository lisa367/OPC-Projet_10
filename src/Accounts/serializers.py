from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import CustomUserModel

# from .models import CustomUserModel

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUserModel
        # fields = "__all__"
        fields = [
            "id",
            "email",
            "first_name",
            "last_name",
            "password",
        ]

    def create(self, validated_data):
        user = User(
            email=validated_data["email"],
            first_name=validated_data["first_name"],
            last_name=validated_data["last_name"],
        )
        user.set_password(validated_data["password"])
        user.save()
        return user

    """ def create(self, validated_data):
        # print(validated_data)
        return super().create(validated_data)
        # return CustomUserModel.objects.create(validated_data) """
