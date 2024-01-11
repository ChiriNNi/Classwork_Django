from django.urls import path
from .views import (  # BbCreateView, BbAddView, IndexView
    BbByRubricView, BbDetailView, BbCreateView, BbEditView, BbDeleteView, BbIndexView, BbMonthView, BbRedirectView)

app_name = 'bboard'

urlpatterns = [
    path('detail/<int:pk>', BbDetailView.as_view(), name='detail'),
    path('update/<int:pk>', BbEditView.as_view(), name='update'),
    path('delete/<int:pk>', BbDeleteView.as_view(), name='delete'),
    path('add/', BbCreateView.as_view(), name='add'),
    path('<int:rubric_id>/', BbByRubricView.as_view(), name="by_rubric"),
    # path('', IndexView.as_view(), name="index"),
    path('', BbIndexView.as_view(), name='index'),
    path('<int:year>/<int:month>/', BbMonthView.as_view(), name='month'),
    path('year/<int:year>/', BbRedirectView.as_view())
]
