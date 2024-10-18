'''
Urls for shortener app urlshortener/urls.py
'''

from django.urls import path
from . import views

urlpatterns = [
    path('', views.shorten_url, name='shorten_url'),
    path('results/', views.shorten_list, name='shorten_list'),
    path('<str:shortened_part>/', views.redirect_url_view, name='redirect_url_view'),
]