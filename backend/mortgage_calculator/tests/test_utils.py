import pytest

from mortgage_calculator.utils import calculate_debt, calculate_payment


@pytest.mark.parametrize(
    'price, initial_fee, term, yearly_rate, payment',
    ([1_000_000, 10, 25, 12.5, 9814],
     [10_000_000, 50, 25, 5.5, 30705],
     [100_000_000, 75, 5, 25.5, 741130],)
)
def test_calculate_payment(price, initial_fee, term, yearly_rate, payment):
    """Расчет аннуитетного платежа выполняется верно"""
    assert calculate_payment(price, initial_fee, term, yearly_rate) == payment


@pytest.mark.parametrize(
    'price, initial_fee, debt',
    ([100_000_000, 10, 90_000_000],
     [2_000_000, 25, 1_500_000],
     [1_234_567, 12, 1_086_419],)
)
def test_calculate_debt(price, initial_fee, debt):
    """Расчет аннуитетного платежа выполняется верно"""
    assert calculate_debt(price, initial_fee) == debt
