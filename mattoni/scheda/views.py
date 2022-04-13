from django.shortcuts import render, redirect
from django.urls import reverse
from django.views import generic
from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.contrib import messages 
from django.forms.models import model_to_dict
from django.conf import settings
from django.core.cache import cache
from scheda.utils import render_to_pdf 

from .forms import MezziCreationForm, MissionCreationForm, MissioneModificaForm, SchedaMissioneForm, UserChangePass, UserModificaForm, UserRegistrationForm, MissioneRifiutoForm, MissioneTrasportoForm
from .models import Missione, MyUser, Mezzo, Scheda, Intervento, TestaPiedi

import datetime
import json
import base64
import os


# Funzioni usate da views
def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


# VIEWS 
def change_theme(request):
    if request.method == 'GET':
        cache.clear()
        data = {}
        tema = request.GET.get('theme')
        request.session['tema'] = tema
        return JsonResponse(data)


class LoginView(generic.View):
    def get(self, request):
        template_name = 'login.html'
        return render(request, template_name)
    
    def access(request):
        username = request.GET['username']
        password = request.GET['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request,user)
            return redirect('home_sc')
        else:
            errors = True
            return render(request, 'login.html', context={'errors':errors})


def modifica_dati(request):
    usr = MyUser.objects.get(username=request.user.username)
    form = UserModificaForm(request.POST or None, instance=usr)
    if request.method == 'POST':
        data = {}
        if form.is_valid():
            form.save()
            data['status'] = 'success'
            messages.success(request, 'Modifiche apportate con successo!')
            return JsonResponse(data)
        else:
            errors = form.errors
            data['errors'] = errors
            data['status'] = 'error'
            return JsonResponse(data)


class HomeSocieta(generic.View):
    def get(self, request):
        template_name = 'home_sc.html'
        mezzi = Mezzo.objects.filter(username=request.user.id)
        mezzitemp = []
        mezziday = []
        for m in mezzi:
            if m.all_day == False:
                mezzitemp.append(m)
            else:
                mezziday.append(m)
        return render(request, template_name, context={'mezzi':mezziday,'mezzitemp':mezzitemp})


class GestioneMezzi(generic.View):
    def get(self, request):
        mezzi = Mezzo.objects.filter(username=request.user.id)
        template_name = 'gestione_mezzi.html'
        return render(request, template_name, context={'mezzi':mezzi})


def mezzi_creation_form(request):
    form = MezziCreationForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        data = {}
        if form.is_valid():
            mezzo = form.save(commit=False)
            user = MyUser.objects.get(username=request.user.username)
            mezzo.username = user
            mezzo.save()
            data['status'] = 'success'
            messages.success(request, 'Mezzo creato con successo!')
            return JsonResponse(data)
        else:
            errors = form.errors
            data['errors'] = errors
            data['status'] = 'error'
            return JsonResponse(data)


class Operativo(generic.View):
    def get(self, request):
        template_name = 'operativo.html'
        return render(request, template_name)


class OperativoRientro(generic.View):
    def get(self, request):
        template_name = 'operativo_rientro.html'
        missione = Missione.objects.get(id_missione=request.session['missione']['id_missione'])
        dict = {'invio' : datetime.datetime.now()}
        d = json.dumps(dict['invio'], default=myconverter)
        d.replace('"', '')
        missione.libero = d[1:17]
        missione.save()
        request.session['missione']['libero'] = d[1:17]
        return render(request, template_name)


def mezzo_scelto(request):
    if request.method == 'GET':
        id = request.GET.get('mezzoscelto')
        if id is None:
            messages.error(request, 'Seleziona un mezzo!')
            return HttpResponseRedirect(reverse('home_sc'))
        else:
            m = Mezzo.objects.get(id_mezzo=id)
            mezzo = {'id_mezzo': m.id_mezzo, 
            'nome': m.nome,
            'tipologia': m.tipologia,
            'all_day': m.all_day,
            'num_mezzo': m.num_mezzo,
            'equip_min': m.equip_min,
            }
            request.session['mezzo'] = mezzo
            return redirect('operativo')


def logout_view(request):
    logout(request)


class RegistrationView(generic.View):
    def get(self, request):
        form = UserRegistrationForm(request.POST or None, request.FILES or None)
        template_name = 'registration.html'
        return render(request, template_name, context={'form': form})


class RegistrationSuccess(generic.View):
    def get(self, request):
        template_name = 'regist_success.html'
        return render(request, template_name)


def registration_request(request):
    form = UserRegistrationForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        data={}
        if form.is_valid():
            user = form.save(commit=False)
            user.save()
            data['status'] = 'success'
            return JsonResponse(data)
        else:
            errors = form.errors
            data['errors'] = errors
            data['status'] = 'error'
            return JsonResponse(data)


def change_password(request):
    form = UserChangePass(request.user, request.POST)
    if request.method == 'POST':
        data = {}
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)
            data['status'] = 'success' 
            messages.success(request, 'La password è stata cambiata correttamente')
            return JsonResponse(data)
        else:
            errors = form.errors
            data['errors'] = errors
            data['status'] = 'error'
            return JsonResponse(data)


def delete_mezzo(request):
    if request.method == 'POST':
        query = Mezzo.objects.get(id_mezzo=request.POST.get('id_mezzo'))
        query.delete()
        messages.success(request, 'Mezzo eliminato correttamente')
        return JsonResponse({})


def missione_creation_form(request):
    form = MissionCreationForm(request.POST or None, request.FILES or None)
    data={}
    if request.method == 'POST':
        if form.is_valid():
            missione = form.save(commit=False)
            scheda = Scheda()
            tp = TestaPiedi()
            tp.save()
            scheda.testa_piedi = tp
            scheda.save()
            dict = {'invio' : datetime.datetime.now()}
            d = json.dumps(dict['invio'], default=myconverter)
            d.replace('"', '')
            missione.invio = d[1:17]
            missione.save()
            dictMissione = model_to_dict(missione)
            dictScheda = model_to_dict(scheda)
            m = request.session['mezzo']
            intervento = Intervento(id_scheda = scheda, id_missione = missione, id_mezzo = Mezzo.objects.get(id_mezzo=m['id_mezzo']))
            intervento.save()
            request.session['missione'] = dictMissione
            request.session['scheda'] = dictScheda
            data['status'] = 'success'
            return JsonResponse(data)
        else:
            errors = form.errors
            data['errors'] = errors
            data['status'] = 'error'
        return JsonResponse(data)
    

def partenza_missione(request):
    template_name = 'partenza_missione.html'
    missione = Missione.objects.get(id_missione=request.session['missione']['id_missione'])
    dict = {'invio' : datetime.datetime.now()}
    d = json.dumps(dict['invio'], default=myconverter)
    d.replace('"', '')
    missione.accetta_missione = d[1:17]
    missione.save()
    request.session['missione']['accetta_missione'] = d[1:17]
    return render(request, template_name)


class AccettaMissione(generic.View):
    def get(self, request):
        template_name = 'accetta_missione.html'
        return render(request, template_name)


class GestioneMissioni(generic.View):
    def get(self, request):
        m = request.session['mezzo']
        intervento = Intervento.objects.filter(id_mezzo= Mezzo.objects.get(id_mezzo=m['id_mezzo']))
        mis = intervento.values_list('id_missione')
        missione = Missione.objects.filter(id_missione__in = mis)
        template_name = 'gestione_missioni.html'
        return render(request, template_name, context={'missione': missione})


class MissioneProtocolli(generic.View):
    def get(self, request):
        template_name = 'missione_protocolli.html'
        missione = Missione.objects.get(id_missione=request.session['missione']['id_missione'])
        dict = {'invio' : datetime.datetime.now()}
        d = json.dumps(dict['invio'], default=myconverter)
        d.replace('"', '')
        missione.partenza = d[1:17]
        missione.save()
        request.session['missione']['partenza'] = d[1:17]
        return render(request, template_name)


class CompilazioneScheda(generic.View):
    def get(self, request):
        template_name = 'mattoni.html'
        missione = Missione.objects.get(id_missione=request.session['missione']['id_missione'])
        dict = {'invio' : datetime.datetime.now()}
        d = json.dumps(dict['invio'], default=myconverter)
        d.replace('"', '')
        missione.arrivo = d[1:17]
        missione.save()
        request.session['missione']['arrivo'] = d[1:17]
        return render(request, template_name)


def dettagli_missione(request, pk):
    template_name = 'dettagli_missione.html'
    if request.method == 'GET':
        query = Missione.objects.get(id_missione=pk)
        intervento = Intervento.objects.get(id_missione=query)
        scheda = Scheda.objects.get(id_scheda = intervento.id_scheda.id_scheda)
        tp = scheda.testa_piedi
        front = str(tp.front)
        fsplit = front.split('/')
        f = fsplit[len(fsplit)-2] + '/' + fsplit[len(fsplit)-1]
        back = str(tp.back)
        bsplit = back.split('/')
        b = bsplit[len(bsplit)-2] + '/' + bsplit[len(bsplit)-1]
        return render(request, template_name, context={'missione': query, 'scheda': scheda, 'front': f, 'back': b})


class RiepilogoMissione(generic.View):
    def get(self, request):
        template_name = 'riepilogo_missione.html'
        if request.method == 'GET':
            missione = Missione.objects.get(id_missione=request.session['missione']['id_missione'])
            scheda = Scheda.objects.get(id_scheda =request.session['scheda']['id_scheda'])
            tp = scheda.testa_piedi
            front = str(tp.front)
            fsplit = front.split('/')
            f = fsplit[len(fsplit)-2] + '/' + fsplit[len(fsplit)-1]
            back = str(tp.back)
            bsplit = back.split('/')
            b = bsplit[len(bsplit)-2] + '/' + bsplit[len(bsplit)-1]
            missione.chiusa = True
            if request.session['missione']['esito'] == True:
                dict = {'invio' : datetime.datetime.now()}
                d = json.dumps(dict['invio'], default=myconverter)
                d.replace('"', '')
                missione.pronto_socc = d[1:17]
                missione.save()
                request.session['missione']['pronto_socc'] = d[1:17]
            else:
                missione.save()
            return render(request, template_name, context={'missione': missione, 'scheda': scheda, 'front': f, 'back': b})


def visualizza_protocollo(request, pk):
    template_name = 'visualizza_protocollo.html'
    return render(request, template_name, context={'nome': pk})


def dati_mezzo(request):
    template_name = 'dati_mezzo.html'
    if request.method == 'GET':
        mezzo = request.session['mezzo']
        return render(request, template_name, context={'mezzo': mezzo})


def invia_scheda(request):
    form = SchedaMissioneForm(request.POST or None, instance=Scheda.objects.get(id_scheda=request.session['scheda']['id_scheda']))
    if request.method == 'POST':
        data = {}
        if form.is_valid():
            scheda = form.save(commit=False)
            scheda.save()
            data['status'] = 'success'
            return JsonResponse(data)
        else:
            errors = form.errors
            data['errors'] = errors
            data['status'] = 'error'
            breakpoint()
            return JsonResponse(data)


def invia_tp(request):
    if request.method == 'POST':
        data = {}
        image_data = request.POST.get('front')
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]
        dataf = ContentFile(base64.b64decode(imgstr))
        front = "front"+str(request.session['scheda']['id_scheda'])+"." + ext
        fs = FileSystemStorage()
        frontname = fs.save(front, dataf)
        scheda = Scheda.objects.get(id_scheda = request.session['scheda']['id_scheda'])
        tp = scheda.testa_piedi
        tp.front = os.path.join(settings.MEDIA_ROOT, frontname)
        image_data = request.POST.get('back')
        format, imgstr = image_data.split(';base64,')
        ext = format.split('/')[-1]
        datab = ContentFile(base64.b64decode(imgstr))
        back = "back"+str(request.session['scheda']['id_scheda'])+"." + ext
        fs = FileSystemStorage()
        backname = fs.save(back, datab)
        tp.back = os.path.join(settings.MEDIA_ROOT, backname)
        tp.save()
        return JsonResponse(data)


def modifica_paziente(request):
    form = MissioneModificaForm(request.POST or None, instance=Missione.objects.get(id_missione=request.session['missione']['id_missione']))
    if request.method == 'POST':
        data = {}
        if form.is_valid():
            missione = form.save(commit=False)
            missione.save()
            data['status'] = 'success'
            return JsonResponse(data)
        else:
            errors = form.errors
            data['errors'] = errors
            data['status'] = 'error'
            return JsonResponse(data)


def rientro_sede(request):
    if request.method == 'GET':
        missione = Missione.objects.get(id_missione=request.session['missione']['id_missione'])
        dict = {'invio' : datetime.datetime.now()}
        d = json.dumps(dict['invio'], default=myconverter)
        d.replace('"', '')
        missione.rientro_sede = d[1:17]
        missione.chiusa = True
        missione.save()
        del request.session['missione']
        del request.session['scheda']
        request.session.modified = True
        data = {}
        return JsonResponse(data)


def partenza_luogo_intervento(request):
    if request.method == 'GET':
        missione = Missione.objects.get(id_missione=request.session['missione']['id_missione'])
        dict = {'invio' : datetime.datetime.now()}
        d = json.dumps(dict['invio'], default=myconverter)
        d.replace('"', '')
        missione.conferma_trasporto = d[1:17]
        missione.save()
        data = {}
        return JsonResponse(data)


def invia_rifiuto(request):
    form = MissioneRifiutoForm(request.POST or None, instance=Missione.objects.get(id_missione=request.session['missione']['id_missione']))
    if request.method == 'POST':
        data = {}
        if form.is_valid():
            missione = form.save(commit=False)
            dict = {'invio' : datetime.datetime.now()}
            d = json.dumps(dict['invio'], default=myconverter)
            d.replace('"', '')
            missione.rifiuto_trasporto = d[1:17]
            missione.esito = False
            request.session['missione']['esito'] = False
            missione.save()
            data['status'] = 'success'
            return JsonResponse(data)
        else:
            errors = form.errors
            data['errors'] = errors
            data['status'] = 'error'
            return JsonResponse(data)


def invia_trasporto(request):
    form = MissioneTrasportoForm(request.POST or None, instance=Missione.objects.get(id_missione=request.session['missione']['id_missione']))
    if request.method == 'POST':
        data = {}
        if form.is_valid():
            missione = form.save(commit=False)
            dict = {'invio' : datetime.datetime.now()}
            d = json.dumps(dict['invio'], default=myconverter)
            d.replace('"', '')
            missione.rientro_sede = d[1:17]
            missione.esito = True
            request.session['missione']['criticita_trasporto'] = missione.criticita_trasporto
            request.session['missione']['patologia_trasporto'] = missione.patologia_trasporto
            request.session['missione']['ospedale'] = missione.ospedale
            request.session['missione']['reparto'] = missione.reparto
            request.session['missione']['esito'] = True
            missione.save()
            data['criticita_trasporto'] = missione.criticita_trasporto
            data['patologia_trasporto'] = missione.patologia_trasporto
            data['ospedale'] = missione.ospedale
            data['reparto'] = missione.reparto
            data['status'] = 'success'
            return JsonResponse(data)
        else:
            errors = form.errors
            data['errors'] = errors
            data['status'] = 'error'
            return JsonResponse(data)
        

class GeneratePdf(generic.View):
    def get(self, request, pk):
        query = Missione.objects.get(id_missione=pk)
        intervento = Intervento.objects.get(id_missione=query)
        scheda = Scheda.objects.get(id_scheda = intervento.id_scheda.id_scheda)
        tp = scheda.testa_piedi
        front = str(tp.front)
        fsplit = front.split('/')
        f = fsplit[len(fsplit)-2] + '/' + fsplit[len(fsplit)-1]
        back = str(tp.back)
        bsplit = back.split('/')
        b = bsplit[len(bsplit)-2] + '/' + bsplit[len(bsplit)-1]
        data = {'missione': query, 'scheda': scheda, 'front': f, 'back': b, 'corp':request.user.corporation}
        pdf = render_to_pdf('pdf/dettagli.html', data)
        if pdf:
            response = HttpResponse(pdf, content_type='application/pdf')
            filename = "Missione_%s.pdf" %(pk)
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse(pdf, content_type='application/pdf')