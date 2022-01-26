from django.shortcuts import get_object_or_404, render, redirect
from django.urls import reverse
from django.http import Http404
from django.template import loader
from django.utils import timezone
from django.views import generic
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, HttpResponseRedirect
from .models import MyUser
from django.contrib.auth.decorators import user_passes_test


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
            else:
                login(request, user)
                return redirect('home_sc')
        else:
            return HttpResponse('<h1>Page was found</h1>')
    

def logout_view(request):
    logout(request)
    #TODO:fare reindirizzamento alla home

class HomesView(generic.View):
    pass