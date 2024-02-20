from django import forms
from django.core import validators
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from captcha.fields import CaptchaField

from .models import Bb as BbModel, Rubric, IceCream


class BbForm(forms.ModelForm):
    title = forms.CharField(label='Название товара',
                            validators=[validators.RegexValidator(regex='^.{4,}$')],
                            error_messages={'invalid': 'Короткое название товара!'})
    content = forms.CharField(label='Описание', widget=forms.widgets.Textarea())
    price = forms.DecimalField(label='Цена', decimal_places=2)
    rubric = forms.ModelChoiceField(
        queryset=Rubric.objects.all(),
        label='Рубрика',
        help_text='Выберите рубрику!',
        widget=forms.widgets.Select(attrs={'size': 8})
    )

    def clean_title(self):
        val = self.cleaned_data.get('title')
        if val == 'Прошлогодний снег':
            raise ValidationError('К продаже не допускается!')
        return val

    def clean(self):
        super().clean()
        errors = {}
        if not self.cleaned_data.get('content'):
            errors['content'] = ValidationError('Укажите описание продоваемого товара')

        if self.cleaned_data.get('price') < 0:
            errors['price'] = ValidationError('Укажите корректное значение продоваемого товара')

        if errors:
            raise ValidationError(errors)

    class Meta:
        model = BbModel
        fields = ('title', 'content', 'price')


class RegisterUserForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль')
    password2 = forms.CharField(label='Пароль (повторно)')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')


class IceCreamForm(forms.ModelForm):
    class Meta:
        model = IceCream
        fields = ('flavor', 'description', 'price', 'available')



class SearchForm(forms.Form):
    keyword = forms.CharField(max_length=20, label="Искомое слово")
    rubric = forms.ModelChoiceField(queryset=Rubric.objects.all(), label="Рубрика")
    captcha = CaptchaField(label='Введите текст с картинки', # error_mesages={'invalid': 'Неправильный текст'},
                           generator='captcha.helpers.word_challenge')

    error_css_class = 'error'
    required_css_class = 'required'