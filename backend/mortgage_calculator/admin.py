from django.contrib import admin

from .models import MortgageOffer


@admin.register(MortgageOffer)
class MortgageOfferAdmin(admin.ModelAdmin):
    list_display = (
        'bank_name',
        'term_min', 'term_max',
        'rate_min', 'rate_max',
        'payment_min', 'payment_max',
    )
