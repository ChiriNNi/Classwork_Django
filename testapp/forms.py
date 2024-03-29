from captcha.fields import CaptchaField
from django import forms
from django.core import validators

from .models import Img, Document, BBCodeText, Course, Student


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


class ImageUploadForm(forms.Form):
    image = forms.ImageField(label='Загрузить изображение')
    thumbnail_size = forms.IntegerField(label='Желаемый размер миниатюры (px)', initial=200)
    captcha = CaptchaField(label='Введите текст с картинки',
                           error_messages={'invalid': 'Неправильный текст'})


class BBCodeForm(forms.ModelForm):
    class Meta:
        model = BBCodeText
        fields = ['bbcode_content']


class CourseForm(forms.ModelForm):
    class Meta:
        model = Course
        fields = ['name']


class StudentForm(forms.ModelForm):
    class Meta:
        model = Student
        fields = ['name', 'courses']