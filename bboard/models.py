from django.core import validators
from django.core.exceptions import ValidationError
from django.db import models

is_all_posts_passive = True


def is_active_default():
    return is_all_posts_passive


def validate_positive(value):
    if value <= 0:
        raise ValidationError('Число %(value)s отрицательное',
                              code='positive',
                              params={'value': value})


def validate_even(value):
    if value % 2 != 0:
        raise ValidationError('Число %(value)s нечетное',
                              code='odd',
                              params={'value': value})


class MinMaxValueValidator:
    def __init__(self, min_value, max_value):
        self.min_value = min_value
        self.max_value = max_value

    def __call__(self, value):
        if value < self.min_value or value > self.max_value:
            raise ValidationError('Введенное число должно находиться в диапазоне от %(min)s до %(max)s',
                                  code='out_of_range',
                                  params={'min': self.min_value, 'max': self.max_value})


class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name="Название", unique=True)
    order = models.SmallIntegerField(default=0, db_index=True)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return f"/{self.pk}/"

    class Meta:
        verbose_name_plural = 'Рубрики'
        verbose_name = 'Рубрика'
        ordering = ['order', 'name']


class Bb(models.Model):
    # class Kinds(models.TextChoices):
    #     BUY = 'b', 'Куплю'
    #     SELL = 's', 'Продам'
    #
    # kind = models.CharField(max_length=1, choices=Kinds.choices, default=Kinds.SELL)

    KINDS = (
        ('b', 'Куплю'),
        ('s', 'Продам'),
        ('c', 'Обменяю'),
    )

    ITEM_STATUSES = (
        ('new', 'Новый'),
        ('used', 'Б/у'),
        ('refurbished', 'Восстановленный'),
    )

    # KINDS = (
    #     ('Купля-продажа', (
    #         ('b', 'Куплю'),
    #         ('s', 'Продам'),
    #     )),
    #     ('Обмен', (
    #         ('c', 'Обменяю'),
    #     ))
    # )

    # KINDS = (
    #     (None, 'Выберите тип объявления'),
    #     ('b', 'Куплю'),
    #     ('s', 'Продам'),
    #     ('c', 'Обменяю'),
    # )

    kind = models.CharField(max_length=1, choices=KINDS, default='s', verbose_name='Тип объявления')
    item_status = models.CharField(max_length=20, choices=ITEM_STATUSES, default='new', verbose_name='Состояние товара')

    rubric = models.ForeignKey("Rubric", null=True, on_delete=models.PROTECT, verbose_name="Рубрика")
    title = models.CharField(
        max_length=50,
        verbose_name="Товар",
        # validators=[validators.RegexValidator(regex='^.{4,}$')],
        # validators=[validators.MinLengthValidator(4),
        #             validators.MinLengthValidator(50)]
    )
    content = models.TextField(null=True, blank=True, verbose_name="Описание", default='Описание: ')
    price = models.DecimalField(max_digits=8,
                                decimal_places=2,
                                verbose_name="Цена",
                                default=0.0,
                                validators=[validators.MinValueValidator(0),
                                              validators.DecimalValidator(8, 2),
                                              # validate_even,
                                              # MinMaxValueValidator(25, 45),
                                              # validate_positive
                                              ])
    is_activate = models.BooleanField(default=is_active_default)
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name="Опубликовано")
    updated = models.DateTimeField(auto_now=True, db_index=True, verbose_name="Изменено")

    def __str__(self):
        return f'{self.title}'

    def clean(self):
        errors = {}
        if not self.content:
            errors['content'] = ValidationError('Укажите описание продаваемого товара')
        if self.price and self.price < 0:
            errors['price'] = ValidationError('Укажите корректное значение цены товара')
        if errors:
            raise ValidationError(errors)

    def title_and_price(self):
        if self.price:
            return f'{self.title} ({self.price:.2f})'
        return self.title

    def id_and_date(self):
        return f'{self.published.strftime("%d.%m.%Y %H:%M:%S")}, id: {self.pk}'

    # title_and_price.short_description = "Название и цена"

    class Meta:
        verbose_name_plural = 'Объявления'
        verbose_name = 'Объявление'
        ordering = ['-published', 'title']
        # order_with_respect_to = 'rubric'