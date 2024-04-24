from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from zs_utils.base_support import constants, models
from zs_utils.user.serializers import UserLightSerializer
from zs_utils.validattors import validate_uuid


__all__ = [
    "CommonSupportTicketSerializer",
    "CommonCreateSupportTicketSerializer",
    "CommonSupportTicketMessageSerializer",
    "CommonCreateSupportTicketMessageSerializer",
    "CommonSupportTicketMessageFileSerializer",
]


class CommonSupportTicketSerializer(serializers.ModelSerializer):
    user = UserLightSerializer()
    manager = UserLightSerializer(read_only=True)

    class Meta:
        model = models.SupportTicket
        fields = [
            "id",
            "number",
            "created",
            "user",
            "manager",
            "status",
            "question_type",
            "subject",
            "unread_messages",
            "client_status"
        ]


class CommonSupportTicketMessageFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.SupportTicketMessageFile
        fields = [
            "id",
            "ticket_message",
            "file",
            "user",
            "name",
        ]


class CommonSupportTicketMessageSerializer(serializers.ModelSerializer):
    sender = UserLightSerializer(read_only=True)
    files = CommonSupportTicketMessageFileSerializer(many=True)

    class Meta:
        model = models.SupportTicketMessage
        fields = [
            "id",
            "created",
            "ticket",
            "sender",
            "text",
            "files",
            "is_system",
            "is_viewed",
        ]


class CommonSupportTicketWithMessagesSerializer(CommonSupportTicketSerializer):
    messages = CommonSupportTicketMessageSerializer(many=True, read_only=True)

    class Meta(CommonSupportTicketSerializer.Meta):
        model = models.SupportTicket
        fields = CommonSupportTicketSerializer.Meta.fields + ["messages"]

    def to_representation(self, instance):
        data = super().to_representation(instance)

        data["user"] = UserLightSerializer(instance.user).data
        data["user"]["phone"] = instance.user.phone

        return data


class CommonCreateSupportTicketMessageSerializer(serializers.Serializer):
    text = serializers.CharField(required=False, allow_null=True)
    files = serializers.ListField(
        child=serializers.SlugRelatedField(
            queryset=models.SupportTicketMessageFile.objects.all(),
            slug_field="id",
            required=False,
        ),
        required=False,
        max_length=constants.MAX_TICKET_MESSAGE_FILES,
    )

    def to_internal_value(self, data):
        print("CommonCreateSupportTicketMessageSerializer", data)
        data = super().to_internal_value(data)
        print("CommonCreateSupportTicketMessageSerializer", data)

        if not (data.get("text") or data.get("files")):
            raise ValidationError({"text": "Обязательное поле, если не задано поле 'files'."})

        return data


class CommonCreateSupportTicketSerializer(serializers.ModelSerializer):
    message = CommonCreateSupportTicketMessageSerializer(required=False)

    class Meta:
        model = models.SupportTicket
        fields = [
            "question_type",
            "subject",
            "message",
        ]

    def to_internal_value(self, data):
        print("CommonCreateSupportTicketSerializer", data)

        if "message" in data and data["message"] is not None:
            message_serializer = self.fields["message"]
            message_internal = message_serializer.to_internal_value(data["message"])
            data["message"] = message_internal
        elif "message" in data and data["message"] is None:
            del data["message"]

        data = super().to_internal_value(data)
        print("CommonCreateSupportTicketSerializer", data)
        return data
