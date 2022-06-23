import pytest
from django.urls import reverse
from mortgage_calculator.models import MortgageOffer
from rest_framework import status
from decimal import Decimal
from mortgage_calculator.utils import calculate_payment

PRICE = 12_000_000
TERM = 25
DEPOSIT = 10
RATE_MIN = 5.5
RATE_MAX = 10.5
PAYMENT_MIN = 50_000
PAYMENT_MAX = 80_000
OFFER_URL = reverse('offer-list')
OFFER_REQUEST_URL = f'{OFFER_URL}?price={PRICE}&deposit={DEPOSIT}&term={TERM}'
OFFER_REQUEST_RATE_MIN_URL = OFFER_REQUEST_URL + f'&rate_min={RATE_MIN}'
OFFER_REQUEST_RATE_MAX_URL = OFFER_REQUEST_URL + f'&rate_max={RATE_MAX}'
OFFER_REQUEST_PAYMENT_MIN_URL = (
    OFFER_REQUEST_URL + f'&payment_min={PAYMENT_MIN}'
)
OFFER_REQUEST_PAYMENT_MAX_URL = (
    OFFER_REQUEST_URL + f'&payment_max={PAYMENT_MAX}'
)
ORDER_RATE = 'rate'
ORDER_RATE_REVERSE = '-rate'


def assert_offer_schema(schema, offer):
    assert schema['bank_name'] == offer.bank_name
    assert schema['term_min'] == offer.term_min
    assert schema['term_max'] == offer.term_max
    assert Decimal(str(schema['rate_min'])) == Decimal(str(offer.rate_min))
    assert Decimal(str(schema['rate_max'])) == Decimal(str(offer.rate_max))
    assert schema['payment_min'] == offer.payment_min
    assert schema['payment_max'] == offer.payment_max


@pytest.mark.django_db
def test_offer_new(guest_client, setup_offer_data):
    """Запрос на создание MortgageOffer создаёт MortgageOffer"""
    assert MortgageOffer.objects.count() == 0
    guest_client.post(OFFER_URL, setup_offer_data, format='json')
    assert MortgageOffer.objects.count() == 1


@pytest.mark.django_db
def test_offer_create(guest_client, setup_offer_data):
    """Запрос на создание MortgageOffer возвращает ожидаемые данные."""
    response = guest_client.post(OFFER_URL, setup_offer_data, format='json')
    assert response.status_code == status.HTTP_201_CREATED
    assert_offer_schema(
        response.data,
        MortgageOffer.objects.get(bank_name=setup_offer_data['bank_name'])
    )
    assert response.data['payment'] is None


@pytest.mark.django_db
def test_offer_partial_update(guest_client, setup_offer,
                              setup_offer_other_data):
    """Запрос на изменение MortgageOffer возвращает ожидаемые данные."""
    OFFER_DETAIL_URL = reverse('offer-detail',
                               args=[setup_offer.id])
    response = guest_client.patch(OFFER_DETAIL_URL,
                                  setup_offer_other_data,
                                  format='json')
    assert_offer_schema(response.data,
                        MortgageOffer.objects.get(id=setup_offer.id))
    assert response.data['payment'] == 0


@pytest.mark.django_db
def test_offer_delete(guest_client, setup_offer):
    """Запрос на удаление MortgageOffer удаляет MortgageOffer."""
    OFFER_DETAIL_URL = reverse('offer-detail',
                               args=[setup_offer.id])
    assert MortgageOffer.objects.count() == 1
    assert guest_client.delete(OFFER_DETAIL_URL).status_code == (
        status.HTTP_204_NO_CONTENT
    )
    assert MortgageOffer.objects.count() == 0


@pytest.mark.django_db
def test_offer_list_all(guest_client, setup_offer):
    """Запрос списка MortgageOffer возвращает ожидаемые данные."""
    assert MortgageOffer.objects.count() == 1
    response = guest_client.get(OFFER_URL)
    assert response.data[0]['id'] == setup_offer.id
    assert_offer_schema(response.data[0], setup_offer)


@pytest.mark.django_db
def test_offer_list_filter(guest_client, setup_offer):
    """Запрос списка MortgageOffer c расчётом возвращает ожидаемые данные."""
    assert MortgageOffer.objects.count() == 1
    response = guest_client.get(OFFER_REQUEST_URL)
    print(response.data)
    assert response.data[0]['payment'] == calculate_payment(
        PRICE, DEPOSIT, TERM, setup_offer.rate_max
    )
    assert_offer_schema(response.data[0], setup_offer)


@pytest.mark.django_db
def test_offer_list_filter_rate_min(guest_client, setup_some_offers):
    """Фильтрация по полю `rate_min` работает верно."""
    response = guest_client.get(OFFER_REQUEST_RATE_MIN_URL)
    for object in response.data:
        assert float(object['rate_min']) >= RATE_MIN


@pytest.mark.django_db
def test_offer_list_filter_rate_max(guest_client, setup_some_offers):
    """Фильтрация по полю `rate_max` работает верно."""
    response = guest_client.get(OFFER_REQUEST_RATE_MAX_URL)
    for object in response.data:
        assert float(object['rate_min']) <= RATE_MAX


@pytest.mark.django_db
def test_offer_list_filter_payment_min(guest_client, setup_some_offers):
    """Фильтрация по полю `payment_min` работает верно."""
    response = guest_client.get(OFFER_REQUEST_PAYMENT_MIN_URL)
    for object in response.data:
        assert int(object['payment']) >= PAYMENT_MIN


@pytest.mark.django_db
def test_offer_list_filter_payment_max(guest_client, setup_some_offers):
    """Фильтрация по полю `payment_max` работает верно."""
    response = guest_client.get(OFFER_REQUEST_PAYMENT_MAX_URL)
    for object in response.data:
        assert int(object['payment']) <= PAYMENT_MAX


@pytest.mark.django_db
def test_offer_list_filter_ordering(guest_client, setup_some_offers):
    """Сортировка по возрастанию по полю `order` работает верно."""
    assert MortgageOffer.objects.count() > 1
    response = guest_client.get(OFFER_REQUEST_URL, {'order': ORDER_RATE})
    rate_now = response.data[0]['rate_max']
    for index in range(1, len(response.data)):
        assert response.data[index]['rate_max'] >= rate_now


@pytest.mark.django_db
def test_offer_list_filter_ordering_reverse(guest_client, setup_some_offers):
    """Сортировка по убыванию по полю `order` работает верно."""
    assert MortgageOffer.objects.count() > 1
    response = guest_client.get(OFFER_REQUEST_URL,
                                {'order': ORDER_RATE_REVERSE})
    rate_now = response.data[0]['rate_max']
    for index in range(1, len(response.data)):
        assert response.data[index]['rate_max'] <= rate_now
