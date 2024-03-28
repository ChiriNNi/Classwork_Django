from django.urls import path

from .views import index, add, get, test_email, add_document

app_name = 'testapp'

urlpatterns = [
    path('', index, name='index'),
    path('add/', add, name='add'),
    path('add_document', add_document, name='add_document'),
    path('get/<path:filename>/', get, name='get'),

    path('mail/', test_email, name='test_email'),
]
