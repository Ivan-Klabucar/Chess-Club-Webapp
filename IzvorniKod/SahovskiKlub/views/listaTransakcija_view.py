from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from ..models import *
from datetime import datetime, date
from django.core import serializers


def render_error(request, message, status_code):
    return render(request, 'error.html', {'err_desc': message}, status=status_code)

class PregledTransakcijaView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render_error(request, 'Morate se prijaviti kako bi pregledali transakcije', 400)
        if not request.user.profil.admin:
            return render_error(request, 'Samo admini imaju pristup listi transakcija', 400)
        transakcije = Transakcija.objects.order_by("-datumTransakcije")
        danasnji_datum = datetime.now()

        if danasnji_datum.strftime("%m") == "1":
            prijasnji_mjesec = 12
        else:
            prijasnji_mjesec = int(danasnji_datum.strftime("%m")) - 1
        zadnji_priznati_dan = danasnji_datum.replace(month=prijasnji_mjesec)
        lista_transakcija_ovaj_mjesec = []
        lista_transakcija_ostalih =[]
        lista_clanova_koji_su_platili = []
        lista_duznika = []

        for transakcija in transakcije:
            transakcija_obj = {
                "platitelj": transakcija.user.username,
                "datum": transakcija.datumTransakcije,
                "iznos": transakcija.iznosUplate
            }
            if transakcija.datumTransakcije >= zadnji_priznati_dan.date():
                lista_transakcija_ovaj_mjesec.append(transakcija_obj)
                lista_clanova_koji_su_platili.append(transakcija.user.id)
            else:
                lista_transakcija_ostalih.append(transakcija_obj)

        users = Profil.objects.filter(trener=False).filter(admin=False).filter(placenaClanarina=True).filter(zabranjenPristup=True)

        for user in users:
            if user.user.id not in lista_clanova_koji_su_platili:
                duznik_obj = {
                    "username": user.user.username,
                    "userid": user.id
                }
                lista_duznika.append(duznik_obj)


        context = {
            "listaTransakcijaPrije": lista_transakcija_ostalih,
            "listaTransakcijaMjesec": lista_transakcija_ovaj_mjesec,
            "listaDuznika": lista_duznika
        }
        return render(request, 'pregledTransakcija.html', context)

class ZabraniPristupView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render_error(request, 'Morate se prijaviti kako bi pregledali transakcije', 400)
        if not request.user.profil.admin:
            return render_error(request, 'Samo admini imaju pristup listi transakcija', 400)
        userid = request.GET.get('id', '')
        if not userid:
            return render_error(request, 'Niste označili korisnika kojemu želite zabraniti pristup', 400)

        user = Profil.objects.get(user=User.objects.get(id=userid))
        user.placenaClanarina = False
        user.save()

        akivnost_string = request.user.username + " je zabranio pristup korisniku \"" + Profil.objects.get(user=User.objects.get(id=userid)).user.username + "\""
        if len(akivnost_string) > 100:
            aktivnost_string = aktivnost_string[0:96] + "..."

        aktivnost = Aktivnost(user=request.user, vrijemeAktivnosti=datetime.now(), aktivnost=aktivnost_string)
        aktivnost.save()

        return redirect('/pregledTransakcija')
