from rest_framework import serializers


class RangeValidator:
    """
    Check range edge fields are correct.
    """
    message = 'Incorrect range: {min} > {max}.'

    def __init__(self, min_field, max_field, message=None):
        self.min_field = min_field
        self.max_field = max_field
        self.message = message or self.message

    def __call__(self, attrs):
        if attrs[self.min_field] > attrs[self.max_field]:
            raise serializers.ValidationError(
                self.message.format(min=str(attrs[self.min_field]),
                                    max=str(attrs[self.max_field]))
            )
