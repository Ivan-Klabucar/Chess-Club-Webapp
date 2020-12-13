from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse

class PregledTransakcijaView(View):
    def get(self, request):
        context = {
            "listaTransakcijaPrije": [
                {
                    "platitelj": "Marko",
                    "datum": "17.8.2019",
                    "iznos": "175"
                },
                {
                    "platitelj": "Ivo",
                    "datum": "19.10.2020",
                    "iznos": "175"
                },
                {
                    "platitelj": "Bruno",
                    "datum": "4.11.2020",
                    "iznos": "175"
                }
            ],
            "listaTransakcijaMjesec": [
                {
                    "platitelj": "Ana",
                    "datum": "11.11.2020",
                    "iznos": "175"
                },
                {
                    "platitelj": "Hrvoje",
                    "datum": "15.11.2020",
                    "iznos": "175"
                },
                {
                    "platitelj": "Bruno",
                    "datum": "7.12.2020",
                    "iznos": "175"
                },
                {
                    "platitelj": "Petar",
                    "datum": "25.11.2020",
                    "iznos": "175"
                }
            ]
        }
        return render(request, 'pregledTransakcija.html', context)