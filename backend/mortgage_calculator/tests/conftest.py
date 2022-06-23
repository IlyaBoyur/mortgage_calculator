import pytest
from rest_framework.test import APIClient

from mortgage_calculator.models import MortgageOffer


@pytest.fixture()
def setup_offer_data(db):
    return {
        'bank_name': 'Test Bank',
        'term_min': 15,
        'term_max': 30,
        'rate_min': 5.5,
        'rate_max': 14.5,
        'payment_min': 1_000_000,
        'payment_max': 15_000_000,
    }


@pytest.fixture()
def setup_offer_other_data(db):
    return {
        'bank_name': 'Test Other Bank',
        'term_min': 7,
        'term_max': 16,
        'rate_min': 8.5,
        'rate_max': 10.5,
        'payment_min': 5_000_000,
        'payment_max': 20_000_000,
    }


@pytest.fixture()
def setup_offer(setup_offer_data):
    return MortgageOffer.objects.create(**setup_offer_data)


@pytest.fixture()
def setup_offer_other(setup_offer_other_data):
    return MortgageOffer.objects.create(**setup_offer_other_data)


@pytest.fixture()
def setup_some_offers(setup_offer_data, setup_offer_other_data):
    return (
        MortgageOffer.objects.create(**setup_offer_data),
        MortgageOffer.objects.create(**setup_offer_other_data),
        MortgageOffer.objects.create(**{
            'bank_name': 'Tiny Test Bank',
            'term_min': 5,
            'term_max': 10,
            'rate_min': 16.5,
            'rate_max': 20.5,
            'payment_min': 500_000,
            'payment_max': 5_000_000,
        }),
        MortgageOffer.objects.create(**{
            'bank_name': 'Huge Test Bank',
            'term_min': 10,
            'term_max': 35,
            'rate_min': 4.5,
            'rate_max': 10.5,
            'payment_min': 10_000_000,
            'payment_max': 500_000_000,
        }),
    )


@pytest.fixture()
def guest_client():
    return APIClient()
