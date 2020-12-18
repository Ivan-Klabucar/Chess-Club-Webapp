from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from ..models import *

class ListaTaktikaView(View):
    def get(self, request):
        taktike = Taktika.objects.filter(vidljivost=True).order_by('id')
        lista_taktika = []

        for taktika in taktike:
            if RjesenjeTaktike.objects.filter(taktika=taktika, user=request.user).exists():
                taktika_obj = {
                    "autor": taktika.user.username,
                    "datum": taktika.createdAt,
                    "idTaktika": taktika.id,
                    "ime": taktika.ime,
                    "vrijeme": RjesenjeTaktike.objects.filter(taktika=taktika, user=request.user).first().vrijeme,
                    "rjeseno": "1"
                }
            else:
                taktika_obj = {
                    "autor": taktika.user.username,
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
            return render_error(request, 'Morate se prijaviti kako bi brisali taktike', 400)
        if not request.user.profil.admin:
            return render_error(request, 'Samo admini imaju pristup brisanju liste taktika', 400)
        taktika_id = request.GET.get('id', '')
        if not taktika_id:
            return render_error(request, 'Niste označili taktiku koju želite obrsiati', 400)
        taktika = Taktika.objects.get(id=taktika_id)
        taktika.vidljivost = False
        taktika.save()
        return redirect('/dnevneTaktike')
