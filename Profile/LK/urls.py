from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from django.views.generic import RedirectView
from .views import *

urlpatterns = [
    path('login/', include('django.contrib.auth.urls')),
    path('login/', LoginUser.as_view(), name='login'),
    path('registration/', SignUpView.as_view(), name='registration'),
    path('', profile, name='profile'),
    path('news/', news, name='news'),
    path('news/<int:news_id>/', view_news, name='view_news'),
    path('create_order', create_order, name='create_order'),
    path('orders', orders, name='orders'),
    path('statistic', stat, name='statistic'),
    path('create_news', create_news, name='create_news'),
    path('sportsmen', sportsmen, name='sportsmen'),
    path('favicon.ico', RedirectView.as_view(url='/static/favicon.png'), name='favicon'),
]