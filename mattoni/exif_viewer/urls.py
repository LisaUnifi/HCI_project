from django.urls import path
from django.contrib import admin
from django.views.generic.base import TemplateView 
import exif_viewer.views as exif

from . import views

urlpatterns = [
    path('', exif.exif, name='exif'),
    path('carica/', exif.carica_img, name='carica'),
    path('cancella/', exif.delete_img, name='cancella'),
    path('cancella_album/', exif.cancella_album, name='cancella_album'),
    path('change_image/<int:pk>', exif.change_image, name='change_image'),
    path('next_image/', exif.next_image, name='next_image'),
    path('previous_image/', exif.previous_image, name='previous_image'),
    path('nuovo_album/', exif.nuovo_album, name='nuovo_album'),
    path('geolocalizzazione/', exif.geolocalizzazione, name='geolocalizzazione'),
    path('filter_image/<int:pk>/', exif.filter_image, name='filter_image'),
    ]