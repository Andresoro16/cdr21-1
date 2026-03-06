from django.urls import path, include
from . import views

""" path = '' """
urlpatterns =[
    path ('',views.principal, name='principal'),
    path ('login', views.login, name='login'),
    path ('home', views.home, name='home'),
    path ('olvide-password', views.olvidePassword, name='olvide-password'),
    path ('testing', views.testing, name="testing"),
]

