from django.shortcuts import render, redirect
from django.contrib import messages 
from django.http import JsonResponse
from matplotlib.pyplot import title
from exif import Image as eim
from PIL import Image as pim
import webbrowser
import os

from .forms import ExifForm, AlbumForm, MapsForm
from .models import Album, ExifImage


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def exif(request):
    if not Album.objects.filter(title='Generico'):
        a = Album(title='Generico')
        a.save()
    img = ExifImage.objects.all()
    album = Album.objects.all()
    template_name = 'exif.html'
    request.session['filter'] = 'all'
    return render(request, template_name, context={'image':img, 'album': album})


def delete_img(request):
    if request.method == 'POST':
        query = ExifImage.objects.get(id=request.POST.get('id'))
        query.delete()
        return JsonResponse({})


def cancella_album(request):
    if request.method == 'POST':
        query = Album.objects.get(id=request.POST.get('id'))
        query.delete()
        return JsonResponse({})


# ESTRAZIONE DEI DATI EXIF DA IMMAGINE TRAMITE LIBRERIA EXIF
def exif_image(img):
    path = os.path.join(BASE_DIR, 'scheda/static/scheda/upload')
    folder = os.path.join(path, img)
    with open(folder, "rb") as file:
        image = eim(file)
    if image.has_exif:
        exif = dir(image)
        data = []
        for element in exif:
            value = image.get(element, 'Non specificato')
            if str(value) != 'Non specificato':
                el = element.replace('_', ' ').title()
                data.append({'key': el, 'value': value})
        lat = maps_coordinate(image.get('gps_latitude', 'Non specificato'), image.get('gps_latitude_ref', 'Non specificato'))
        lon = maps_coordinate(image.get('gps_longitude', 'Non specificato'), image.get('gps_longitude_ref', 'Non specificato'))
        return data, lat, lon
    else:
        return {}, '', ''


# ESTRAZIONE FORMATO IMMAGINE 
def exif_extract(img):
    path = os.path.join(BASE_DIR, 'scheda/static/scheda/upload')
    folder = os.path.join(path, img)
    image = pim.open(folder)
    data = []
    data = [
        {'key': 'Formato', 'value': image.format},
    ]
    return data


# COVERSIONE COORDINATE LATITUDINE E LONGITUDINE 
def maps_coordinate(coordinates, coordinates_ref):
    if coordinates != 'Non specificato':
        decimal_degrees = coordinates[0] + \
                        coordinates[1] / 60 + \
                        coordinates[2] / 3600
    
        if coordinates_ref == "S" or coordinates_ref == "W":
            decimal_degrees = -decimal_degrees
    
        return decimal_degrees
    else:
        return 'Non specificato'


def change_image(request, pk=0):
    if request.method == 'GET':
        if pk == 0:
            selected = ExifImage.objects.first()
        else:
            selected = ExifImage.objects.get(id=pk)
        if request.session['filter'] == 'all':
            img = ExifImage.objects.all()
        else:
            id = Album.objects.get(id=request.session['filter'])
            img = ExifImage.objects.filter(album=id)
            if selected.album != id:
                selected = img.first()
        exif, lat, lon = exif_image(str(selected.img))
        otherexif = exif_extract(str(selected.img))
        numero = len(exif)
        sel = str(selected.img.url)
        url = sel.replace('/media/exif/', '')
        album = Album.objects.all()
        template_name = 'exif.html'
        return render(request, template_name, context={'image': img, 'album': album, 'selected': selected, 'url': url, 'exif': exif, 'lat': lat, 'lon': lon, 'other': otherexif, 'numero': numero})


def filter(request):
    if request.method == 'GET':
        request.session['filter'] = request.GET.get('id')
        return JsonResponse({})


def next_image(request):
    if request.method == 'GET':
        data={}
        if request.session['filter'] == 'all':
            img = ExifImage.objects.all()
        else:
            id = Album.objects.get(id=request.session['filter'])
            img = ExifImage.objects.filter(album=id)
        j = 0
        pk = -1
        val = int(request.GET.get('id'))
        for i in img:
            if val == j:
                pk = int(i.id)
            j = i.id
        if pk == -1:
            el = img[0]
            pk = int(el.id)
        data['status'] = 'success'
        data['pk'] = pk
        return JsonResponse(data)


def previous_image(request):
    if request.method == 'GET':
        data={}
        if request.session['filter'] == 'all':
            img = ExifImage.objects.all()
        else:
            id = Album.objects.get(id=request.session['filter'])
            img = ExifImage.objects.filter(album=id)
        j = -1
        pk = -1
        val = int(request.GET.get('id'))
        for i in img:
            if val == int(i.id):
                pk = j
            j = i.id
        if pk == -1:
            el = img[len(img)-1]
            pk = int(el.id)
        data['status'] = 'success'
        data['pk'] = pk
        return JsonResponse(data)


def carica_img(request):
    form = ExifForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        data={}
        if form.is_valid():
            if request.POST.get('album') != '':
                album = Album.objects.get(id = request.POST.get('album'))
            else:
                album = Album.objects.get(title = 'Generico')
            img = form.save(commit = False)
            img.album = album
            img.save()
            data['status'] = 'success'
            selected = ExifImage.objects.get(id=img.id)
            exif, lat, lon = exif_image(str(selected.img))
            numero = len(exif)
            sel = str(selected.img.url)
            url = sel.replace('/media/exif/', '')
            img = ExifImage.objects.all()
            album = Album.objects.all()
            template_name = 'exif.html'
            return render(request, template_name, context={'image': img, 'album': album, 'selected': selected, 'url': url, 'exif': exif, 'lat': lat, 'lon': lon, 'numero': numero})
        else:
            errors = form.errors
            data['errors'] = errors
            data['status'] = 'error'
            messages.warning(request, '')
            return redirect('exif')


# COSTRUZIONE DELLA MAPPA SU GOOGLE MAPS
def geolocalizzazione(request):
    form = MapsForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            mappa = request.POST.get('map')
            lat = request.POST.get('latitude')
            lon = request.POST.get('longitude')
            data = {}
            if mappa == 'map':
                zoom = request.POST.get('zoom')
                basemap = request.POST.get('basemap')
                layer = request.POST.get('layer')
                path = 'https://www.google.com/maps/@?api=1&map_action=map&center='+lat+'%2C'+lon+'&zoom='+zoom+'&basemap='+basemap+'&layer='+layer
            elif mappa == 'pano':
                pitch = request.POST.get('pitch')
                fov = request.POST.get('fov')
                path = 'https://www.google.com/maps/@?api=1&map_action=pano&viewpoint='+lat+'%2C'+lon+'&pitch='+pitch+'&fov='+fov
            else:
                path = 'https://www.google.com/maps/search/?api=1&query='+lat+'%2C'+lon
            webbrowser.open_new_tab(path)
            data['status'] = 'success'
            return JsonResponse(data)
        else:
            return redirect('exif')


def nuovo_album(request):
    form = AlbumForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        data={}
        if form.is_valid():
            element = form.save(commit = False)
            a = Album.objects.filter(title = Album.objects.last())
            id = a[0].id + 1
            element.id = id
            element.save()
            data['status'] = 'success'
            return JsonResponse(data)
        else:
            errors = form.errors
            data['errors'] = errors
            data['status'] = 'error'
            return JsonResponse(data)
