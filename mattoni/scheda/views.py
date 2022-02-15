from re import S
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.http import Http404
from django.template import loader, RequestContext
from django.utils import timezone
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse

from .forms import MezziCreationForm, MissionCreationForm, UserRegistrationForm
from .models import Missione, MyUser, Mezzo, Scheda, Intervento, TestaPiedi
from django.contrib import messages 
from django.contrib.auth.decorators import user_passes_test, login_required
from django.forms.models import model_to_dict
import datetime
import json


import pdb


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
            return HttpResponse('<h1>User not found</h1>')



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
            errors = form.errors
            data['errors'] = errors
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

'''
def mezzo_scelto(request):
    if request.method == 'GET':
            m = Mezzo.objects.get(id_mezzo=request.GET.get('mezzoscelto'))
            mezzo = {'id_mezzo': m.id_mezzo, 
            'nome': m.nome,
            'tipologia': m.tipologia,
            'all_day': m.all_day,
            'num_mezzo': m.num_mezzo,
            'equip_min': m.equip_min,
            }
            request.session['mezzo'] = mezzo
            return redirect('operativo')

'''
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
            
            missione.save()
            scheda = Scheda()
            tp = TestaPiedi()
            tp.save()
            scheda.testa_piedi = tp
            scheda.save()
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


def dettagli_missione(request, pk):
    template_name = 'dettagli_missione.html'
    if request.method == 'GET':
        query = Missione.objects.get(id_missione=pk)
        intervento = Intervento.objects.get(id_missione=query)
        scheda = Scheda.objects.get(id_scheda = intervento.id_scheda.id_scheda)
        return render(request, template_name, context={'missione': query, 'scheda': scheda})


def visualizza_protocollo(request, pk):
    template_name = 'visualizza_protocollo.html'
    return render(request, template_name, context={'nome': pk})


def dati_mezzo(request):
    template_name = 'dati_mezzo.html'
    if request.method == 'GET':
        mezzo = request.session['mezzo']
        return render(request, template_name, context={'mezzo': mezzo})


