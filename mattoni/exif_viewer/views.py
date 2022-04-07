from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import ListView
from .forms import ExifForm, AlbumForm, MapsForm
from django.conf import settings
from django.contrib import messages 

import os
import matplotlib.pyplot as plt
from exif import Image as eim
from PIL import Image as pim

import webbrowser


from .models import Album, ExifImage


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def exif(request):
    ''' CAPIRE COME PASSARE ID DELL'ALBUM '''
    if request.GET.get('id'):
        id = Album.objects.get(id = request.GET.get('id'))
        img = ExifImage.objects.filter(album=id)
        album = Album.objects.all()
        data = {}
        data['status'] = 'success'
        return JsonResponse(data)
        ''' CAPIRE COME PASSARE OGGETTI: FORSE HTTPRESPONSEREDIRECT? '''
    else:
        img = ExifImage.objects.all()
        album = Album.objects.all()
        template_name = 'exif.html'
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

        ''' GUARDA SE FARE UN MESSAGGIO IN ALTO '''
        return JsonResponse({})


''' VALUTARE SE COMPLETARE CALCOLO EXIF CON ALTRA LIBRERIA '''
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

def exif_extract(img):
    path = os.path.join(BASE_DIR, 'scheda/static/scheda/upload')
    folder = os.path.join(path, img)
    image = pim.open(folder)
    data = []
    data = [
        {'key': 'Formato', 'value': image.format},
    ]
    return data


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


def RED(R): return '#%02x%02x%02x'%(R,0,0)
def GREEN(G): return '#%02x%02x%02x'%(0,G,0)
def BLUE(B):return '#%02x%02x%02x'%(0,0,B)

def image_histogram(img):
    path = os.path.join(BASE_DIR, 'scheda/static/scheda/upload')
    spath = os.path.join(BASE_DIR, 'scheda/static/scheda/histogram')
    folder = os.path.join(path, img)
    image = pim.open(folder)
    histogram = image.histogram()
    l1 = histogram[0:256]
    l2 = histogram[256:512]
    l3 = histogram[512:768]
    plt.figure(0)
    for i in range(0, 256):
        plt.bar(i, l1[i], color = RED(i), edgecolor=RED(i), alpha=0.3)
    plt.savefig(os.path.join(spath, 'red.png'))
    plt.figure(1)
    for i in range(0, 256):
        plt.bar(i, l2[i], color = GREEN(i), edgecolor=GREEN(i),alpha=0.3)
    plt.savefig(os.path.join(spath, 'green.png'))
    plt.figure(2)
    for i in range(0, 256):
        plt.bar(i, l3[i], color = BLUE(i), edgecolor=BLUE(i),alpha=0.3)
    plt.savefig(os.path.join(spath, 'blue.png'))


''' FIXA CHANGE IMAGE PERCHé FA SCOMPARIRE IL FILTRO '''
def change_image(request, pk):
    if request.method == 'GET':
        selected = ExifImage.objects.get(id=pk)
        exif, lat, lon = exif_image(str(selected.img))
        otherexif = exif_extract(str(selected.img))
        #image_histogram(str(selected.img))
        numero = len(exif)
        sel = str(selected.img.url)
        url = sel.replace('/media/exif/', '')
        img = ExifImage.objects.all()
        album = Album.objects.all()
        template_name = 'exif.html'
        return render(request, template_name, context={'image': img, 'album': album, 'selected': selected, 'url': url, 'exif': exif, 'lat': lat, 'lon': lon, 'other': otherexif, 'numero': numero})


def next_image(request):
    if request.method == 'GET':
        data={}
        img = ExifImage.objects.all()
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
        img = ExifImage.objects.all()
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
            album = Album.objects.get(id = request.POST.get('album'))
            img = form.save(commit = False)
            img.album = album
            img.save()
            data['status'] = 'success'
            
            selected = ExifImage.objects.get(id=img.id)
            exif, lat, lon = exif_image(str(selected.img))
            #image_histogram(str(selected.img))
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
            return redirect('exif')


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


def filter_image(request, pk):
    if request.method == 'GET':
        id = Album.objects.get(id=pk)
        img = ExifImage.objects.filter(album=id)
        album = Album.objects.all()
        template_name = 'exif.html'
        return render(request, template_name, context={'image':img, 'album': album})


def nuovo_album(request):
    form = AlbumForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        data={}
        if form.is_valid():
            form.save()
            data['status'] = 'success'
            return JsonResponse(data)
        else:
            errors = form.errors
            data['errors'] = errors
            data['status'] = 'error'
            return JsonResponse(data)
