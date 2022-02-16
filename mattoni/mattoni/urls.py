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
    path('gestione_mezzi/', scheda.GestioneMezzi.as_view(), name='gestione_mezzi'),
    path('crea_mezzo/', scheda.mezzi_creation_form, name='crea_mezzo'),
    path('mezzo_scelto/', scheda.mezzo_scelto, name='mezzo_scelto'),
    path('delete_mezzo/<int:pk>/', scheda.delete_mezzo, name='delete_mezzo'),
    path('operativo/', scheda.Operativo.as_view(), name='operativo'),
    path('invia_missione/', scheda.missione_creation_form, name='invia_missione'),
    path('accetta_missione/', scheda.AccettaMissione.as_view(), name='accetta_missione'),

    path('dati/', TemplateView.as_view(template_name='dati.html'), name='dati'),
    path('modifica_dati/', scheda.modifica_dati, name='modifica_dati'),
    path('gestione_missioni/', scheda.GestioneMissioni.as_view(), name='gestione_missioni'),
    path('dettagli_missione/<int:pk>/', scheda.dettagli_missione, name='dettagli_missione'),
    path('visualizza_protocollo/<str:pk>/', scheda.visualizza_protocollo, name='visualizza_protocollo'),
    path('protocolli/', TemplateView.as_view(template_name='protocolli.html'), name='protocolli'),
    path('dati_mezzo/', scheda.dati_mezzo, name='dati_mezzo'),
    path('partenza_missione/', scheda.partenza_missione, name='partenza_missione'),
    path('missione_protocolli/', scheda.MissioneProtocolli.as_view(), name='missione_protocolli'),
    path('mattoni/', scheda.CompilazioneScheda.as_view(), name='mattoni'),
    path('invia_scheda/', scheda.invia_scheda, name='invia_scheda'),
]
