from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponse
from ..models import Profil, User, Transakcija
from datetime import datetime

def render_error(request, message, status_code):
    return render(request, 'error.html', {'err_desc': message}, status=status_code)

class PlacanjeClanarineView(View):
    def get(self, request):
        context = {}
        user_profil = Profil.objects.get(user=request.user)
        if (user_profil.placenaClanarina):
            return render_error(request, 'Clanarina je vec placena', 400)
        return render(request, 'placanjeClanarine.html', context)

    def post(self, request):
        user_curr = request.user
        new_transakcija = Transakcija(user=user_curr, datumTransakcije=datetime.now(), iznosUplate=100)
        new_transakcija.save()
        user_profil = Profil.objects.get(user=request.user)
        user_profil.placenaClanarina = True
        user_profil.save()
        return redirect('/profil')
        