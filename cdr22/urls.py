from django.urls import path
from . import views

""" path = '' """
urlpatterns =[
    path ('',views.principal, name='principal'),
    path ('login', views.login, name='login'),
]

