from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path
from .views import (  # BbCreateView, BbAddView, IndexView, BbIndexView,
    index, BbByRubricView, BbDetailView, BbCreateView, BbEditView, BbDeleteView, BbMonthView,
    UserProfileView, AllUsersView, select_columns, exclude_values, rubrics, bbs)

app_name = 'bboard'

urlpatterns = [
    path('detail/<int:pk>', BbDetailView.as_view(), name='detail'),
    path('update/<int:pk>', BbEditView.as_view(), name='update'),
    path('delete/<int:pk>', BbDeleteView.as_view(), name='delete'),
    path('add/', BbCreateView.as_view(), name='add'),
    path('<int:rubric_id>/', BbByRubricView.as_view(), name="by_rubric"),
    path('select_columns/', select_columns, name="select_columns"),
    path('exclude_values/', exclude_values, name="exclude_values"),
    # path('', IndexView.as_view(), name="index"),
    # path('', BbIndexView.as_view(), name='index'),
    path('', index, name='index'),
    path('<int:year>/<int:month>/', BbMonthView.as_view(), name='month'),

    path('all_users/', AllUsersView.as_view(), name='all_users'),
    path('user_profile/<int:pk>/', UserProfileView.as_view(), name='user_profile'),

    path('rubrics/', rubrics, name='rubrics'),
    path('bbs/<int:rubric_id>/', bbs, name="bbs"),
    path('accounts/login/', LoginView.as_view(), name='login'),
    path('accounts/logout/', LogoutView.as_view(), name='logout')
]
