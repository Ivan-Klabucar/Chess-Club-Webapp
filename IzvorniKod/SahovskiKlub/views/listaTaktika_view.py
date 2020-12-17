from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from ..models import *

class ListaTaktikaView(View):
    def get(self, request):
        taktike = Taktika.objects.order_by('id')
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