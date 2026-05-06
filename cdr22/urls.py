from django.urls import path, include
from . import views
from django.contrib.auth.views import LoginView, LogoutView

""" path = '' """
urlpatterns =[
    path ('',views.principal, name='principal'),
    path ('login', views.login_view, name='login'),
    path ('olvide-password', views.olvidePassword, name='olvide-password'),
    path ('testing', views.testing, name="testing"),
    path ('login-django', LoginView.as_view(template_name='login.html'), name='logindjango'),
    
    path('dashboard/home', views.home, name='home'),
    path('dashboard/productos/', views.productos_index, name='productos_index'),
    path('dashboard/productos/crear/', views.productos_crear, name='productos_crear'),
    path('dashboard/productos/editar/<int:producto_id>/', views.productos_editar, name='productos_editar'),
    path('dashboard/productos/eliminar/<int:producto_id>/', views.productos_eliminar, name='productos_eliminar'),

]

