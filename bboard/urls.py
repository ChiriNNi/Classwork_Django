from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from django.views.decorators.cache import cache_page

from .views import (index,
                    BbIndexView, BbMonthView, BbByRubricView,
                    BbCreateView, BbDetailView, BbEditView, BbDeleteView,
                    BbRedirectView, edit, add_save, rubrics, bbs, search, api_rubrics, api_rubrics_detail, api_bbs)


app_name = 'bboard'

urlpatterns = [
    path('api/rubrics/<int:pk>/', api_rubrics_detail),
    path('api/rubrics/', api_rubrics),

    path('api/bbs/', api_bbs),

    path('detail/<int:pk>/', BbDetailView.as_view(), name='detail'),
    path('add/save/', add_save, name='add_save'),
    path('add/', BbCreateView.as_view(), name='add'),
    path('update/<int:pk>/', BbEditView.as_view(), name='update'),
    # path('update/<int:pk>/', edit, name='update'),
    path('delete/<int:pk>/', BbDeleteView.as_view(), name='delete'),

    path('<int:rubric_id>/', BbByRubricView.as_view(), name='by_rubric'),
    # path('<int:rubric_id>/', cache_page(10)(BbByRubricView.as_view()), name='by_rubric'),

    path('', index, name='index'),
    # path('', BbIndexView.as_view(), name='index'),
    path('year/<int:year>/', BbRedirectView.as_view(), name='redirect'),
    path('<int:year>/<int:month>/', BbMonthView.as_view(), name='month'),

    path('rubrics/', rubrics, name='rubrics'),
    path('bbs/<int:rubric_id>/', bbs, name='bbs'),

    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout'),

    path('search/', search, name='search'),
]
