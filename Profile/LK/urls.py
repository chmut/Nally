from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import RedirectView
from .views import *

urlpatterns = [
    path('login/', include('django.contrib.auth.urls')),
    path('login/', LoginUser.as_view(), name='login'),
    path('registration/', SignUpView.as_view(), name='registration'),
    # path('dop_registration/', SignUpDop.as_view(), name='dop_registration'),
    path('', profile, name='profile'),
    path('settings/<int:pk>', Profile.as_view(), name='settings'),
    path('news/', news, name='news'),
    path('news/<int:news_id>/', view_news, name='view_news'),
    path('create_order/', create_order, name='create_order'),
    path('orders/', orders, name='orders'),
    path('statistic/', stat, name='statistic'),
    path('statistic_admin/', create_statistic, name='statistic_admin'),
    path('statistic_admin/<int:group_id>/', get_group_stat, name='group_stat'),
    path('create_news/', create_news, name='create_news'),
    path('sportsmen/', sportsmen, name='sportsmen'),
    path('sportsmen/group/<int:group_id>/', sportsmen_group, name='sportsmen_group'),
    path('sportsmen/filial/<int:filial_id>/', sportsmen_filial, name='sportsmen_filial'),
    path('sportsmen/<int:pk>', SportsmenUpdate.as_view(), name='sportsmen_update'),
    # path('groups/', Groups.as_view(), name='groups'),
    path('groups/', groups, name='groups'),
    path('filial/<int:filial_id>', filials, name='filial'),
    path('groups/new', CreateGroup.as_view(), name='create_group'),
    path('groups/<int:pk>', GroupUpdate.as_view(), name='group_update'),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.png'), name='favicon'),
]