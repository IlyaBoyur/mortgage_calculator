import pytest
from django.urls import reverse

OFFER_URL = reverse('offer-list')
PRICE = 12_000_000
TERM = 25
DEPOSIT = 10
OFFER_REQUEST_URL = f'{OFFER_URL}?price={PRICE}&term={TERM}&deposit={DEPOSIT}'


@pytest.mark.django_db
def test_users_url_exists_at_desired_location(setup_offer, guest_client,
                                              subtests):
    """Страницы возвращают ожидаемый код ответа соответствующему клиенту."""
    OFFER_DETAIL_URL = reverse('offer-detail',
                               args=[setup_offer.id])
    urls = [
        [OFFER_URL, guest_client, 200],
        [OFFER_REQUEST_URL, guest_client, 200],
        [OFFER_DETAIL_URL, guest_client, 200],
    ]
    for url, client, response_code in urls:
        with subtests.test(url=url):
            assert client.get(url).status_code == response_code
