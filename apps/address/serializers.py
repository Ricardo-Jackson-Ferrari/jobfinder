from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from rest_framework import serializers

from .models import Address


class AddressSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(
        read_only=True, default=serializers.CurrentUserDefault()
    )

    def validate(self, data):
        if self.context['request'].method != 'PATCH':
            instance = Address(user=self.context['request'].user, **data)
            try:
                instance.full_clean()
            except ValidationError as e:
                raise serializers.ValidationError(e.args[0]) from e
        return data

    class Meta:
        model = Address
        fields = '__all__'
        validators = [
            serializers.UniqueTogetherValidator(
                queryset=model.objects.all(),
                fields=('user', 'title'),
                message=_('You already have an address with that title'),
            )
        ]
