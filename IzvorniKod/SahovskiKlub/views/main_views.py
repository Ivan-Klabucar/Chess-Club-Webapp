from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponseForbidden
from ..models import DojavaPogreske, User, Novost
from datetime import datetime

def render_error(request, message, status_code):
    return render(request, 'error.html', {'err_desc': message}, status=status_code)

class HomeView(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.profil.zabranjenPristup:
            return HttpResponseForbidden()
        return render(request, 'homepage.html')

class RegisterView(View):
    def get(self, request):
        context = {}
        form = UserCreationForm(request.POST or None)
        context['form'] = form
        return render(request, 'registration/sign_up.html', context)

    def post(self, request):
        context = {}
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return render(request, 'homepage.html')
        context['form'] = form
        return render(request, 'registration/sign_up.html', context)
