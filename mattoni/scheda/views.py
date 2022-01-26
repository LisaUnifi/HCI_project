from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.http import Http404
from django.template import loader, RequestContext
from django.utils import timezone
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect

from .forms import UserRegistrationForm
from .models import MyUser
from django.contrib import messages 
from django.contrib.auth.decorators import user_passes_test

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
            if operator_check(user):
                login(request, user)
                return redirect('home_op')
            elif staff_check(user):
                return redirect('home_socc')
            else:
                return redirect('home_sc')

        else:
            return HttpResponse('<h1>Page was found</h1>')
    

def logout_view(request):
    logout(request)
    redirect('home')




def registration_request(request):
    form = UserRegistrationForm(request.POST or None, request.FILES or None)
    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)

            user_type = form.cleaned_data['user_type']
            if user_type == 'staff':
                user.staff = True
            elif user_type == 'operator':
                user.is_operator = True
            
            user.save()
            return render(request, 'regist_success.html')
        else:
            print(form.errors)
            #TODO:funziona ma devo aggiungere un metodo per controllare i dati e gli errori
            #return HttpResponse('<h1>Form Not valid</h1>')
    return render(request, 'registration.html', {'form': form})
    

