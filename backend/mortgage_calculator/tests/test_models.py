def test_offer_verbose_names(setup_offer):
    """MortgageOffer: verbose_name в полях совпадает с ожидаемым"""
    field_verboses = {
        'bank_name': 'Наименование банка',
        'term_min': 'Срок ипотеки, ОТ',
        'term_max': 'Срок ипотеки, ДО',
        'rate_min': 'Ставка, ОТ',
        'rate_max': 'Ставка, ДО',
        'payment_min': 'Сумма кредита, ОТ',
        'payment_max': 'Сумма кредита, ДО',
    }
    for field, value in field_verboses.items():
        assert setup_offer._meta.get_field(field).verbose_name == value
    assert setup_offer._meta.verbose_name == 'Ипотечное предложение'
    assert setup_offer._meta.verbose_name_plural == 'Ипотечные предложения'
    assert str(setup_offer) == (
        f'{setup_offer.bank_name}, '
        f'{setup_offer.rate_min}-{setup_offer.rate_max}'
    )
