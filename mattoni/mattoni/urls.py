"""mattoni URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from django.views.generic.base import TemplateView 
import scheda.views as scheda

urlpatterns = [
    #path include nella prima parte il nome della pagina e nella seconda il contenuto 
    path('', include('django.contrib.auth.urls')),
    path('', TemplateView.as_view(template_name='home.html'), name='home'),
    path('scheda/', include('scheda.urls')),
    path('loginpage/', scheda.LoginView.as_view(), name='loginpage'),
    path('access/', scheda.LoginView.access, name='access'),
    path('admin/', admin.site.urls),
    path('logout/', scheda.logout_view, name='logout'),
    path("registration_user/", scheda.registration_request, name="registration_user"),
    #TODO: da togliere
    path('home_op/', TemplateView.as_view(template_name='home_op.html'), name='home_op'),
    path('home_sc/', scheda.HomeSocieta.as_view(), name='home_sc'),
    path('mattoni/', TemplateView.as_view(template_name='mattoni.html'), name='mattoni'),
    path('gestione_mezzi/', scheda.GestioneMezzi.as_view(), name='gestione_mezzi'),
    path('crea_mezzo/', scheda.mezzi_creation_form, name='crea_mezzo'),
]
