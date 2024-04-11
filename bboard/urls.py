from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path, include
from django.views.decorators.cache import cache_page
from rest_framework.routers import DefaultRouter

from .views import (index,
                    BbIndexView, BbMonthView, BbByRubricView,
                    BbCreateView, BbDetailView, BbEditView, BbDeleteView,
                    BbRedirectView, edit, add_save, rubrics, bbs, search, api_rubrics, api_rubrics_detail, api_bbs,
    # APIRubrics, APIRubricsDetail
                    APIRubricViewSet, api_bbs_detail, )


app_name = 'bboard'

router = DefaultRouter()
router.register('rubrics', APIRubricViewSet)

urlpatterns = [
    # path('api/v1/rubrics/<int:pk>/', api_rubrics_detail),
    # path('api/v1/rubrics/<int:pk>/', APIRubricsDetail.as_view()),

    path('api/v1/rubrics/', api_rubrics),
    # path('api/v1/rubrics/', APIRubrics.as_view()),

    # api/v1/rubrics/ - GET, POST
    # api/v1/rubrics/pk/ - GET, PUT, PATCH, DELETE
    path('api/', include(router.urls)),

    path('api/bbs/', api_bbs),
    path('api/bbs/<int:pk>/', api_bbs_detail),

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
