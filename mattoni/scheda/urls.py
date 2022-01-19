from django.urls import path

from . import views

urlpatterns = [
    path('loginpage/', views.LoginView.as_view(), name='loginpage'),
    path('access/', views.LoginView.access, name='access'),
    ]