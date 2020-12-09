from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponse


class HomeView(View):
    def get(self, request):
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


class RemoveListView(View):
    def get(self, request):
        context = {
            "članovi": [
                {
                    "ime": "Marko",
                    "zadnjaTransakcija": "11.2020."
                },
                {
                    "ime": "Ivo",
                    "zadnjaTransakcija": "10.2020."
                }
            ]
        }
        return render(request, 'removeLista.html', context)


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


class ProfileView(View):
    def get(self, request):
        context = {
            "uloga": "Član kluba",
            "listaAktivnosti": [
                {
                    "tekstAktivnosti": "30.11. Riješena taktika xy."
                },
                {
                    "tekstAktivnosti": "1.12. Prijavljen na trening xy."
                },
                {
                    "tekstAktivnosti": "2.12. Riješena taktika z."
                }
            ]
        }
        return render(request, 'profil.html', context)


class NovostiView(View):
    def get(self, request):
        context = {
            "listaNovosti": [
                {
                    "autor": "Trener1",
                    "datum": "10.12.2020",
                    "naslov": "Klub mijenja lokaciju",
                    "tekst": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc ex metus, dignissim eget mi nec, ullamcorper auctor diam. Donec tincidunt massa quis risus vulputate sollicitudin. Curabitur iaculis mattis tempor. Suspendisse finibus ante sit amet finibus sodales. Proin porttitor fringilla tellus vitae dignissim. Morbi eget massa metus. Proin mollis tellus quis dignissim pulvinar. Nam suscipit nisi mattis nisi euismod consectetur. Sed nec nisl placerat, imperdiet nunc a, ultricies mi. Morbi eget fermentum neque. Quisque et erat ante. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas."
                },
                {
                    "autor": "Trener2",
                    "datum": "5.12.2020",
                    "naslov": "Otkazani treninzi Trenera2",
                    "tekst": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc ex metus, dignissim eget mi nec, ullamcorper auctor diam. Donec tincidunt massa quis risus vulputate sollicitudin. Curabitur iaculis mattis tempor. Suspendisse finibus ante sit amet finibus sodales. Proin porttitor fringilla tellus vitae dignissim. Morbi eget massa metus. Proin mollis tellus quis dignissim pulvinar. Nam suscipit nisi mattis nisi euismod consectetur. Sed nec nisl placerat, imperdiet nunc a, ultricies mi. Morbi eget fermentum neque. Quisque et erat ante. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas."
                },
                {
                    "autor": "Admin",
                    "datum": "1.12.2020",
                    "naslov": "Uplata članarine",
                    "tekst": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc ex metus, dignissim eget mi nec, ullamcorper auctor diam. Donec tincidunt massa quis risus vulputate sollicitudin. Curabitur iaculis mattis tempor. Suspendisse finibus ante sit amet finibus sodales. Proin porttitor fringilla tellus vitae dignissim. Morbi eget massa metus. Proin mollis tellus quis dignissim pulvinar. Nam suscipit nisi mattis nisi euismod consectetur. Sed nec nisl placerat, imperdiet nunc a, ultricies mi. Morbi eget fermentum neque. Quisque et erat ante. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas."
                }
            ],
        }
        return render(request, 'novosti.html', context)



class ObjavaNovostiView(View):
    def get(self, request):
        context = {}
        return render(request, 'objavaNovosti.html', context)

    def post(self, request):
        print(request.POST.get('title'))
        print(request.POST.get('text'))
        return redirect('/novosti')



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
