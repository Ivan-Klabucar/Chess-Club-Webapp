from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse, HttpResponseForbidden

from . import render_error
from ..models import *
from datetime import datetime

class ListaTaktikaView(View):
    def get(self, request):
        if request.user.is_authenticated and request.user.profil.zabranjenPristup:
            return HttpResponseForbidden()
        if request.user.is_authenticated and not request.user.profil.admin and not request.user.profil.trener and not request.user.profil.placenaClanarina and not request.user.profil.zabranjenPristup:
            return redirect('/placanjeClanarine')

        taktike = Taktika.objects.filter(vidljivost=True).order_by('-createdAt')
        lista_taktika = []

        for taktika in taktike:
            if request.user.is_authenticated:
                if RjesenjeTaktike.objects.filter(taktika=taktika, user=request.user).exists():
                    taktika_obj = {
                        "autor": taktika.user.username,
                        "autor_id": taktika.user.id,
                        "datum": taktika.createdAt,
                        "idTaktika": taktika.id,
                        "ime": taktika.ime,
                        "vrijeme": RjesenjeTaktike.objects.filter(taktika=taktika, user=request.user).first().vrijeme,
                        "rjeseno": "1"
                    }
                else:
                    taktika_obj = {
                        "autor": taktika.user.username,
                        "autor_id": taktika.user.id,
                        "datum": taktika.createdAt,
                        "idTaktika": taktika.id,
                        "ime": taktika.ime
                    }
            else:
                taktika_obj = {
                    "autor": taktika.user.username,
                    "autor_id": taktika.user.id,
                    "datum": taktika.createdAt,
                    "idTaktika": taktika.id,
                    "ime": taktika.ime
                }
            lista_taktika.append(taktika_obj)

        context = {
            "listaTaktika": lista_taktika
        }
        return render(request, 'listaDnevnihTaktika.html', context)

class ObrisiTaktikuView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render_error(request, 'Samo admini imaju pristup brisanju taktika', 400)
        if request.user.profil.zabranjenPristup:
            return HttpResponseForbidden()
        if not request.user.profil.admin and not request.user.profil.trener and not request.user.profil.placenaClanarina and not request.user.profil.zabranjenPristup:
            return redirect('/placanjeClanarine')
        if not request.user.profil.admin:
            return render_error(request, 'Samo admini imaju pristup brisanju taktika', 400)
        taktika_id = request.GET.get('id', '')
        if not taktika_id:
            return render_error(request, 'Niste označili taktiku koju želite obrsiati', 400)
        taktika = Taktika.objects.get(id=taktika_id)
        taktika.vidljivost = False
        taktika.save()

        aktivnost_string="Brisanje taktike \"" + Taktika.objects.get(id=taktika_id).ime + "\""
        if len(aktivnost_string) > 100:
            aktivnost_string = aktivnost_string[0:96] + "..."

        aktivnost = Aktivnost(user=request.user, vrijemeAktivnosti=datetime.now(), aktivnost=aktivnost_string)
        aktivnost.save()

        return redirect('/dnevneTaktike')
