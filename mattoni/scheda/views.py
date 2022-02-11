from re import S
from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse, reverse_lazy
from django.http import Http404
from django.template import loader, RequestContext
from django.utils import timezone
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect

from .forms import MezziCreationForm, MissionCreationForm, UserRegistrationForm
from .models import Missione, MyUser, Mezzo
from django.contrib import messages 
from django.contrib.auth.decorators import user_passes_test, login_required
import datetime


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
        mezzi = Mezzo.objects.filter(username=request.user.id)
        template_name = 'gestione_mezzi.html'
        form = MezziCreationForm(request.POST or None, request.FILES or None)
        if request.method == 'POST':
            if form.is_valid():
                mezzo = form.save(commit=False)

                user = MyUser.objects.get(username=request.user.username)
                mezzo.username = user
                
                mezzo.save()
                messages.success(request, 'Mezzo creato con successo!')
                return redirect('gestione_mezzi')
            else:
                return render(request, template_name, {'form': form, 'mezzi':mezzi})
        return render(request, template_name, {'form': form, 'mezzi':mezzi})


class Operativo(generic.View):
    def get(self, request):
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
            template_name = 'operativo.html'
            return render(request, template_name)



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
            return redirect('accetta_missione')
        else:
            print(form.errors)
            #TODO:funziona ma devo aggiungere un metodo per controllare i dati e gli errori
            #return HttpResponse('<h1>Form Not valid</h1>')
    return render(request, '', {'form': form})


class AccettaMissione(generic.View):
    def get(self, request):
        template_name = 'accetta_missione.html'
        return render(request, template_name)


class GestioneMissioni(generic.View):

    def get(self, request):
        missione = Missione.objects.filter(username=request.user.id)
        template_name = 'gestione_missioni.html'
        return render(request, template_name, context={'missione': missione})

    """ APRI MISSIONE DA FARE """