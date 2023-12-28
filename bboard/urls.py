from django.urls import path, re_path
from .views import (index, by_rubric, BbCreateView,
    # add, add_save,
                    add_and_save, BbByRubricView, IndexView)

app_name='bboard'

urlpatterns = [
    # path('add/save/', add_save(), name='add_save'),
    # path('add/', add, name="add"),

    path('add/', BbCreateView.as_view(), name='add'),
    # path('<int:rubric_id>/', by_rubric, name="by_rubric"),
    path('<int:rubric_id>/', BbByRubricView.as_view(), name="by_rubric"),
    path('', IndexView.as_view(), name="index"),

    # re_path(r'^add/$', BbCreateView.as_view(), name='add'),
    # re_path(r'^(?P<rubric_id>[0-9]*)/$', by_rubric, name="by_rubric"),
    # re_path(r'^$', index, name="index")
]
