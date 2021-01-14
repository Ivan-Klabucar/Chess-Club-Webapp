from django.shortcuts import render
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


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

class ListaTaktikaView(View):
    def get(self, request):
        context = {
            "listaTaktika" : [
                {
                    "autor" : "Marko",
                    "datum" : "17.8.2019"
                },
                {
                    "autor" : "Ivo",
                    "datum" : "19.10.2020"
                }
            ],
            "listaTaktikeIstaknute" : [
                {
                    "autor" : "Bruno",
                    "datum" : "19.10.2021"
                }
            ]
        }
        return render(request, 'listaDnevnihTaktika.html', context)

class NovostiView(View):
    def get(self, request):
        context = {
            "listaNovosti" : [
                {
                                "autor" : "Trener1",
                                "datum" : "10.12.2020",
                                "naslov": "Klub mijenja lokaciju",
                                "tekst" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc ex metus, dignissim eget mi nec, ullamcorper auctor diam. Donec tincidunt massa quis risus vulputate sollicitudin. Curabitur iaculis mattis tempor. Suspendisse finibus ante sit amet finibus sodales. Proin porttitor fringilla tellus vitae dignissim. Morbi eget massa metus. Proin mollis tellus quis dignissim pulvinar. Nam suscipit nisi mattis nisi euismod consectetur. Sed nec nisl placerat, imperdiet nunc a, ultricies mi. Morbi eget fermentum neque. Quisque et erat ante. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas."
                },
                {
                                "autor" : "Trener2",
                                "datum" : "5.12.2020",
                                "naslov": "Otkazani treninzi Trenera2",
                                "tekst" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc ex metus, dignissim eget mi nec, ullamcorper auctor diam. Donec tincidunt massa quis risus vulputate sollicitudin. Curabitur iaculis mattis tempor. Suspendisse finibus ante sit amet finibus sodales. Proin porttitor fringilla tellus vitae dignissim. Morbi eget massa metus. Proin mollis tellus quis dignissim pulvinar. Nam suscipit nisi mattis nisi euismod consectetur. Sed nec nisl placerat, imperdiet nunc a, ultricies mi. Morbi eget fermentum neque. Quisque et erat ante. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas."
                },
                {
                                "autor" : "Admin",
                                "datum" : "1.12.2020",
                                "naslov": "Uplata članarine",
                                "tekst" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc ex metus, dignissim eget mi nec, ullamcorper auctor diam. Donec tincidunt massa quis risus vulputate sollicitudin. Curabitur iaculis mattis tempor. Suspendisse finibus ante sit amet finibus sodales. Proin porttitor fringilla tellus vitae dignissim. Morbi eget massa metus. Proin mollis tellus quis dignissim pulvinar. Nam suscipit nisi mattis nisi euismod consectetur. Sed nec nisl placerat, imperdiet nunc a, ultricies mi. Morbi eget fermentum neque. Quisque et erat ante. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas."
                }
                        ],
                }
        return render(request, 'novosti.html', context)

class DemoTacticView(View):
    def get(self, request):
        context = {
            'tactic_data': {
                'start_position': 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR',
                'white_moves': ['d4', 'e4', 'f4', 'exd5', 'Bxf4'],
                'black_moves': ['d5', 'e5', 'f5', 'exf4']
            }
        }
        return render(request, 'tactic.html', context)
