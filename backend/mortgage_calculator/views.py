from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.response import Response

from .filters import MortgageOfferFilter
from .models import MortgageOffer
from .serializers import (
    MortgageOfferFilteredSerializer, MortgageOfferReadSerializer,
    MortgageOfferWriteSerializer,
)


class MortgageOfferViewSet(viewsets.ModelViewSet):
    http_method_names = ['post', 'patch', 'get', 'delete']
    queryset = MortgageOffer.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MortgageOfferFilter

    def get_serializer_class(self):
        """Customize serializer class based on action"""
        if self.action in ('create', 'update', 'partial_update'):
            return MortgageOfferWriteSerializer
        elif self.action in ('retrieve', 'list'):
            if self.is_filter_request():
                return MortgageOfferFilteredSerializer
            return MortgageOfferReadSerializer
        return super().get_serializer_class()

    def list(self, request, *args, **kwargs):
        """Customize serializer data"""
        queryset = self.filter_queryset(self.get_queryset())
        serializer_data = self.get_serializer(queryset, many=True).data

        if self.is_filter_request():
            payment_min = self.request.query_params.get('payment_min')
            if payment_min is not None:
                serializer_data = (obj for obj in serializer_data
                                   if obj['payment'] > int(payment_min))
            payment_max = self.request.query_params.get('payment_max')
            if payment_max is not None:
                serializer_data = (obj for obj in serializer_data
                                   if obj['payment'] < int(payment_max))
        return Response(serializer_data)

    def is_filter_request(self):
        """Check request triggers mortgage payment calculation or not"""
        return (self.request.query_params.get('price')
                and self.request.query_params.get('deposit')
                and self.request.query_params.get('term'))
