from django import forms
from django.core import validators

from .models import Img, Document, BBCodeText


class ImgForm(forms.ModelForm):
    img = forms.ImageField(label='Изображение',
                           validators=[
                               validators.FileExtensionValidator(
                                   allowed_extensions=('gif', 'jpg', 'png'))],
                           error_messages={
                               'invalid_extension': 'Этот формат не поддерживается'})
    desc = forms.CharField(label='Описание',
                           widget=forms.widgets.Textarea())

    class Meta:
        model = Img
        fields = '__all__'


class DocumentForm(forms.ModelForm):
    title = forms.CharField(label='Тема')
    file = forms.FileField(label='Файл',
                           validators=[
                               validators.FileExtensionValidator(
                                   allowed_extensions=('xlsx', 'pdf'))],
                           error_messages={
                               'invalid_extension': 'Этот формат не поддерживается'})

    class Meta:
        model = Document
        fields = ['title', 'file']


class BBCodeForm(forms.ModelForm):
    class Meta:
        model = BBCodeText
        fields = ['bbcode_content']
