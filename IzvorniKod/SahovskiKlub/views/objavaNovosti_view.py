from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponse
from SahovskiKlub.models import DojavaPogreske, User, Novost
from datetime import datetime

class ObjavaNovostiView(View):
    def get(self, request):
        user = request.user
        if not (user.is_superuser or user.is_staff):
            return render_error(request, "Nemate ovlasti za objavu", 400)
        context = {}
        return render(request, 'objavaNovosti.html', context)

    def post(self, request):
        user_curr = request.user
        new_novost = Novost(user = user_curr, vrijemeObjave = datetime.now(), naslov = request.POST.get('title'), tekst = request.POST.get('text'))
        new_novost.save()
        return redirect('/novosti')