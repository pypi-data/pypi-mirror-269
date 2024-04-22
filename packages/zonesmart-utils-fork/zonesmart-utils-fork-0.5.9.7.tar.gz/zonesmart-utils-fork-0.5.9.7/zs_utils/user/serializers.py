from django.contrib.auth import get_user_model
from rest_framework import serializers


__all__ = [
    "UserLightSerializer",
]

User = get_user_model()


class UserLightSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            "id",
            "identifier",
            "email",
        ]
