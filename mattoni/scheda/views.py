from re import S
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.http import Http404
from django.template import loader, RequestContext
from django.utils import timezone
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from django.core.serializers import serialize
from django.core.serializers.json import DjangoJSONEncoder
from django.core.files.base import ContentFile
from django.core.files.storage import FileSystemStorage
from django.core.files import File
from .forms import MezziCreationForm, MissionCreationForm, MissioneModificaForm, SchedaMissioneForm, UserModificaForm, UserRegistrationForm, MissioneRifiutoForm, MissioneTrasportoForm
from .models import Missione, MyUser, Mezzo, Scheda, Intervento, TestaPiedi
from django.contrib import messages 
from django.contrib.auth.decorators import user_passes_test, login_required
from django.forms.models import model_to_dict
from django.conf import settings

import datetime
import json
import base64
import os
import io
from django.http import FileResponse
from scheda.utils import render_to_pdf #created in step 4


import pdb



def myconverter(o):
    if isinstance(o, datetime.datetime):
        return o.__str__()


def operator_check(user):
    return user.is_operator

def staff_check(user):
    return user.is_staff

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

            user = form.save()

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
        for m in mezzi:
            if m.all_day == False:
                mezzitemp.append(m)
        return render(request, template_name, context={'mezzi':mezzi,'mezzitemp':mezzitemp})


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

  #  nell'HTML:
    



def logout_view(request):
    logout(request)
    redirect('home')




def registration_request(request):
    form = UserRegistrationForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            
            user.save()
            return render(request, 'regist_success.html')
        else:
            print(form.errors)
            #TODO:funziona ma devo aggiungere un metodo per controllare i dati e gli errori
            #return HttpResponse('<h1>Form Not valid</h1>')
    return render(request, 'registration.html', {'form': form})


def delete_mezzo(request, pk):
    if request.method == 'POST':
        query = Mezzo.objects.get(id_mezzo=pk)
        query.delete()
        messages.success(request, 'Mezzo eliminato correttamente')
        return redirect('gestione_mezzi')


def missione_creation_form(request):
    form = MissionCreationForm(request.POST or None, request.FILES or None)
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
            return redirect('accetta_missione')
        else:
            print(form.errors)
            #TODO:funziona ma devo aggiungere un metodo per controllare i dati e gli errori
            #return HttpResponse('<h1>Form Not valid</h1>')
    return render(request, '', {'form': form})


# TODO: fix il problema con la pagina
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
            return render(request, template_name, context={'missione': missione, 'scheda': scheda})


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
            
            #messages.success(request, 'Scheda salvata!')
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
            #messages.success(request, 'Scheda salvata!')
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
            filename = "Invoice_%s.pdf" %("12341231")
            content = "inline; filename='%s'" %(filename)
            download = request.GET.get("download")
            if download:
                content = "attachment; filename='%s'" %(filename)
            response['Content-Disposition'] = content
            return response
        return HttpResponse(pdf, content_type='application/pdf')