from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponseForbidden
from ..models import DojavaPogreske, Profil, User, Novost, Aktivnost
from datetime import datetime

class NovostiView(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.profil.zabranjenPristup:
            return HttpResponseForbidden()
        novosti = Novost.objects.filter(vidljivost=True).order_by('-vrijemeObjave')
        lista_novosti = []
        for novost in novosti:
            novost_obj = {
                "autor" : novost.user.username,
                "datum" : novost.vrijemeObjave,
                "naslov" : novost.naslov,
                "tekst" : novost.tekst,
                "id" : novost.id
            }

            lista_novosti.append(novost_obj)

        context = {
            "listaNovosti": lista_novosti,
        }
        return render(request, 'novosti.html', context)

    def post(self, request):
        user_curr = request.user
        curr_novost = Novost.objects.filter(id=request.POST.get('brisanje')).update(vidljivost=False)
        new_aktivnost = Aktivnost(user = user_curr, vrijemeAktivnosti = datetime.now(), aktivnost="Brisanje novosti")
        new_aktivnost.save()
        return redirect ('/novosti')