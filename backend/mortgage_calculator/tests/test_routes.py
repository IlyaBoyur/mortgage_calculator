from django.urls import reverse


def test_routes(setup_offer, subtests):
    """URL-адрес, рассчитанный через имя,
    соответствует ожидаемому видимому URL."""
    routes = {
        # Static URLs
        '/api/offer/': reverse('offer-list'),
        # Non static generated URLs
        f'/api/offer/{setup_offer.id}/': reverse('offer-detail',
                                                 args=[setup_offer.id]),
    }
    for url, reversed_url in routes.items():
        with subtests.test(url=url, reversed_url=reversed_url):
            assert url == reversed_url
