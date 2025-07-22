from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing_page, name='landing_page'),
    path('irc/', views.irc_client, name='irc_client'),
path('status/', views.admin_status, name='admin_status'),
]
