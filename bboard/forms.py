from django import forms
from django.contrib.auth.models import User

from .models import Bb, Rubric


# BbForm = modelform_factory(
#     Bb,
#     fields = ('title', 'content', 'price', 'rubric'),
#     labels = ['titlte', 'Название товара'],
#     help_texts = {'rubric': 'Выберите рубрику!'},
#     field_classes = {'price', DecimalField},
#     widgets={'rubric': Select{attrs=['size':8})}
# )


class BbForm(forms.ModelForm):
    title = forms.CharField(label='Название товара')
    content = forms.CharField(label='Описание', widget=forms.widgets.Textarea())
    price = forms.DecimalField(label='Цена', decimal_places=2)
    rubric = forms.ModelChoiceField(
        queryset=Rubric.objects.all(),
        label='Рубрика',
        help_text='Выберите рубрику!',
        widget=forms.widgets.Select(attrs={'size': 8})
    )

    class Meta:
        model = Bb
        fields = ('title', 'content', 'price', 'rubric')


class RegisterUserForm(forms.ModelForm):
    password1 = forms.CharField(label='Пароль')
    password2 = forms.CharField(label='Пароль (повторно)')

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name')