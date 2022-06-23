from rest_framework import serializers
from .models import MortgageOffer
from .validators import RangeValidator
from .utils import calculate_payment

ERROR_PAYMENT_RANGE = (
    'Минимальная сумма кредита больше максимальной: {min} > {max}'
)
ERROR_RATE_RANGE = (
    'Минимальная ставка по ипотеке больше максимальной: {min} > {max}'
)
ERROR_TERM_RANGE = (
    'Минимальный срок ипотеки больше максимального: {min} > {max}'
)


class MortgageOfferWriteSerializer(serializers.ModelSerializer):
    payment = serializers.SerializerMethodField()

    class Meta:
        model = MortgageOffer
        fields = '__all__'
        validators = (
            RangeValidator(
                min_field='term_min',
                max_field='term_max',
                message=ERROR_TERM_RANGE,
            ),
            RangeValidator(
                min_field='rate_min',
                max_field='rate_max',
                message=ERROR_RATE_RANGE,
            ),
            RangeValidator(
                min_field='payment_min',
                max_field='payment_max',
                message=ERROR_PAYMENT_RANGE,
            ),
        )

    def get_payment(self, obj):
        return (
            None if self.context['request'].method == 'POST'
            else 0
        )


class MortgageOfferReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = MortgageOffer
        fields = '__all__'


class MortgageOfferFilteredSerializer(serializers.ModelSerializer):
    payment = serializers.SerializerMethodField()

    class Meta:
        model = MortgageOffer
        fields = '__all__'

    def get_payment(self, obj):
        return calculate_payment(
            int(self.context['request'].query_params['price']),
            int(self.context['request'].query_params['deposit']),
            int(self.context['request'].query_params['term']),
            float(obj.rate_max),
        )
