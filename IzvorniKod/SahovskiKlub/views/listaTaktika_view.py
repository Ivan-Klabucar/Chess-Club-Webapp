from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse

class ListaTaktikaView(View):
    def get(self, request):
        context = {
            "listaTaktika": [
                {
                    "autor": "Marko",
                    "datum": "17.8.2019"
                },
                {
                    "autor": "Ivo",
                    "datum": "19.10.2020"
                }
            ],
            "listaTaktikeIstaknute": [
                {
                    "autor": "Bruno",
                    "datum": "19.10.2021"
                }
            ]
        }
        return render(request, 'listaDnevnihTaktika.html', context)