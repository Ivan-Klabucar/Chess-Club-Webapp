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

class TreninziView(View):
    def get(self, request):
        context = {
            "listaTreninga": [
                {
                    "idTreninga": "12",
                    "organizator": "Trener1",
                    "vrijemePocetka": "16:00",
                    "vrijemeZavrsetka": "18:00",
                    "datum": "10.12.2020.",
                    "opis": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc ex metus, dignissim eget mi nec, ullamcorper auctor diam. Donec tincidunt massa quis risus vulputate sollicitudin. Curabitur iaculis mattis tempor. Suspendisse finibus ante sit amet finibus sodales. Proin porttitor fringilla tellus vitae dignissim. Morbi eget massa metus. Proin mollis tellus quis dignissim pulvinar. Nam suscipit nisi mattis nisi euismod consectetur. Sed nec nisl placerat, imperdiet nunc a, ultricies mi. Morbi eget fermentum neque. Quisque et erat ante. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas."
                },
                {
                    "idTreninga": "34",
                    "organizator": "Trener2",
                    "vrijemePocetka": "16:00",
                    "vrijemeZavrsetka": "18:00",
                    "datum": "11.12.2020.",
                    "opis": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc ex metus, dignissim eget mi nec, ullamcorper auctor diam. Donec tincidunt massa quis risus vulputate sollicitudin. Curabitur iaculis mattis tempor. Suspendisse finibus ante sit amet finibus sodales. Proin porttitor fringilla tellus vitae dignissim. Morbi eget massa metus. Proin mollis tellus quis dignissim pulvinar. Nam suscipit nisi mattis nisi euismod consectetur. Sed nec nisl placerat, imperdiet nunc a, ultricies mi. Morbi eget fermentum neque. Quisque et erat ante. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas."
                },
                {
                    "idTreninga": "56",
                    "organizator": "Trener3",
                    "vrijemePocetka": "16:00",
                    "vrijemeZavrsetka": "18:00",
                    "datum": "12.12.2020.",
                    "opis": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc ex metus, dignissim eget mi nec, ullamcorper auctor diam. Donec tincidunt massa quis risus vulputate sollicitudin. Curabitur iaculis mattis tempor. Suspendisse finibus ante sit amet finibus sodales. Proin porttitor fringilla tellus vitae dignissim. Morbi eget massa metus. Proin mollis tellus quis dignissim pulvinar. Nam suscipit nisi mattis nisi euismod consectetur. Sed nec nisl placerat, imperdiet nunc a, ultricies mi. Morbi eget fermentum neque. Quisque et erat ante. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas."
                }
            ],
        }
        return render(request, 'treninzi.html', context)

    def post(self, request):
        print(request.POST.get('idUsera'))
        print(request.POST.get('idTreninga'))
        return redirect('/treninzi')

class ObjavaNovostiView(View):
    def get(self, request):
        context = {}
        return render(request, 'objavaNovosti.html', context)

    def post(self, request):
        print(request.POST.get('title'))
        print(request.POST.get('text'))
        return redirect('/novosti')




