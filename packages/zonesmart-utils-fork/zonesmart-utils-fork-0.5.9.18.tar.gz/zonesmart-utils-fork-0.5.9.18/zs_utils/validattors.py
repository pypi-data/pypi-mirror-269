import uuid

from rest_framework.exceptions import ValidationError


def validate_uuid(value):
    try:
        uuid.UUID(str(value))
    except ValueError:
        raise ValidationError("Неверный формат UUID.")
