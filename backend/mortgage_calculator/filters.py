from django_filters import FilterSet, NumberFilter, OrderingFilter

from .utils import calculate_debt


class MortgageOfferFilter(FilterSet):
    term_min = NumberFilter(field_name='term_min', lookup_expr='gte')
    term_max = NumberFilter(field_name='term_max', lookup_expr='lte')
    rate_min = NumberFilter(field_name='rate_min', lookup_expr='gte')
    rate_max = NumberFilter(field_name='rate_max', lookup_expr='lte')
    order = OrderingFilter(
        fields=(
            ('rate_max', 'rate'),
        ),
    )

    @property
    def qs(self):
        term = self.request.query_params.get('term')
        price = self.request.query_params.get('price')
        deposit = self.request.query_params.get('deposit')
        if (term is not None and price is not None and deposit is not None):
            debt = calculate_debt(
                int(price),
                int(deposit),
            )
            return super().qs.filter(
                term_min__lte=term,
                term_max__gte=term,
                payment_min__lte=debt,
                payment_max__gte=debt,
            )
        return super().qs
