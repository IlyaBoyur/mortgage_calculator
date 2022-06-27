import math
from sys import argv


def calculate_payment(price, initial_fee, term, yearly_rate):
    """Calculate mortgage monthly payment

    A = D * r * (1 + r)^n / ((1 + r)^n - 1), where
    A - monthly payment,
    D - full debt,
    r - monthy rate,
    n - number of payments.
    D = p * (1 - f), where
    p - mortage subject price,
    f - initial fee in %
    """
    monthly_rate = yearly_rate / 12 / 100
    full_rate = pow(1 + monthly_rate, term * 12)
    return math.ceil(
        calculate_debt(price, initial_fee) * monthly_rate * full_rate
        / (full_rate - 1)
    )


def calculate_debt(price, initial_fee):
    """Calculate mortgage debt

    D = p * (1 - f), where
    p - mortage subject price,
    f - initial fee in %
    """
    return math.ceil(price - price * 0.01 * initial_fee)


if __name__ == '__main__':
    print(f'Ипотека')
    print('---------------')
    print(f'Цена квартиры, ₽: {int(argv[1]):,}')
    print(f'Первоначальный взнос, %: {argv[2]}')
    print(f'Срок, лет: {argv[3]}')
    print(f'Ставка, %: {argv[4]}')
    print('---------------')
    print(f'Ежемесячный платёж, ₽:'
          f'{calculate_payment(*(float(value) for value in argv[1:]))}')
