from django.db import models
from django.core.exceptions import ValidationError


class MortgageOffer(models.Model):
    bank_name = models.CharField(
        'Наименование банка',
        max_length=200,
        unique=True,
    )
    term_min = models.PositiveIntegerField(
        'Срок ипотеки, ОТ',
    )
    term_max = models.PositiveIntegerField(
        'Срок ипотеки, ДО',
    )
    rate_min = models.DecimalField(
        'Ставка, ОТ',
        max_digits=4,
        decimal_places=2,
    )
    rate_max = models.DecimalField(
        'Ставка, ДО',
        max_digits=4,
        decimal_places=2,
    )
    payment_min = models.PositiveIntegerField(
        'Сумма кредита, ОТ',
    )
    payment_max = models.PositiveIntegerField(
        'Сумма кредита, ДО',
    )

    class Meta:
        verbose_name = 'Ипотечное предложение'
        verbose_name_plural = 'Ипотечные предложения'

    def __str__(self):
        return f'{self.bank_name}, {self.rate_min}-{self.rate_max}'

    def clean(self) -> None:
        if self.term_min > self.term_max:
            raise ValidationError(
                'Минимальный срок ипотеки больше максимального.'
            )
        if self.rate_min > self.rate_max:
            raise ValidationError(
                'Минимальная ставка по ипотеке больше максимальной.'
            )
        if self.payment_min > self.payment_max:
            raise ValidationError(
                'Минимальная сумма кредита больше максимальной.'
            )
        return super().clean()
