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
                'start_position': 'rnbqkbnr/pppppppp/8/8/7P/8/PPPPPPPB/RNBQK1NR w KQkq - 0 1',
                'white_moves': ['d4', 'e4', 'f4', 'exd5', 'Bcxf4'],
                'black_moves': ['d5', 'e5', 'f5', 'exf4']
            }
        }
        return render(request, 'taktika.html', context)

class TacticCreationView(View):
    def get(self, request):
        context = {}
        return render(request, 'objavaTaktike.html', context)
    
    def post(self, request):
      print("bijeli potezi:")
      print(request.POST.get('white_moves', ''))
      print("crni potezi:")
      print(request.POST.get('black_moves', ''))
      print("init config:")
      print(request.POST.get('init_config', ''))
      return HttpResponse('sve pet')

class TacticRevisionView(View):
    def get(self, request):
        context = {
            'tactic_data': {
                'id': 74,
                'old_start_position': 'rnbqkbnr/pppppppp/8/8/7P/8/PPPPPPPB/RNBQK1NR w KQkq - 0 1',
                'old_white_moves': ['d4', 'e4', 'f4', 'exd5', 'Bcxf4'],
                'old_black_moves': ['d5', 'e5', 'f5', 'exf4'],
                'new_start_position': 'rnbqkbnr/pppppppp/8/8/7P/8/PPPPPPPB/RNBQK1NR w KQkq - 0 1',
                'new_white_moves': ['d4', 'e4', 'f4', 'fxe5', 'Bh6'],
                'new_black_moves': ['d5', 'e5', 'f5', 'fxe4']
            }
        }
        return render(request, 'revidiranjeTaktike.html', context)
    
    def post(self, request):
      if request.POST.get('confirmed', '') == 'true':
        print("Revision #{} was confirmed".format(request.POST.get('id', '')))
      else:
        print("Revision #{} was rejected".format(request.POST.get('id', '')))
      return HttpResponse('sve pet')



class TreninziView(View):
    def get(self, request):
        context = {
            "listaTreninga" : [
                {
                                "organizator" : "Trener1",
                                "vrijemePocetka" : "16:00",
                                "vrijemeZavrsetka": "18:00",
								"datum": "10.12.2020.",
                                "opis" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc ex metus, dignissim eget mi nec, ullamcorper auctor diam. Donec tincidunt massa quis risus vulputate sollicitudin. Curabitur iaculis mattis tempor. Suspendisse finibus ante sit amet finibus sodales. Proin porttitor fringilla tellus vitae dignissim. Morbi eget massa metus. Proin mollis tellus quis dignissim pulvinar. Nam suscipit nisi mattis nisi euismod consectetur. Sed nec nisl placerat, imperdiet nunc a, ultricies mi. Morbi eget fermentum neque. Quisque et erat ante. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas."
                },
                {
                                "organizator" : "Trener2",
                                "vrijemePocetka" : "16:00",
                                "vrijemeZavrsetka": "18:00",
								"datum": "11.12.2020.",
                                "opis" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc ex metus, dignissim eget mi nec, ullamcorper auctor diam. Donec tincidunt massa quis risus vulputate sollicitudin. Curabitur iaculis mattis tempor. Suspendisse finibus ante sit amet finibus sodales. Proin porttitor fringilla tellus vitae dignissim. Morbi eget massa metus. Proin mollis tellus quis dignissim pulvinar. Nam suscipit nisi mattis nisi euismod consectetur. Sed nec nisl placerat, imperdiet nunc a, ultricies mi. Morbi eget fermentum neque. Quisque et erat ante. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas."
                },
                {
                                "organizator" : "Trener3",
                                "vrijemePocetka" : "16:00",
                                "vrijemeZavrsetka": "18:00",
								"datum": "12.12.2020.",
                                "opis" : "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc ex metus, dignissim eget mi nec, ullamcorper auctor diam. Donec tincidunt massa quis risus vulputate sollicitudin. Curabitur iaculis mattis tempor. Suspendisse finibus ante sit amet finibus sodales. Proin porttitor fringilla tellus vitae dignissim. Morbi eget massa metus. Proin mollis tellus quis dignissim pulvinar. Nam suscipit nisi mattis nisi euismod consectetur. Sed nec nisl placerat, imperdiet nunc a, ultricies mi. Morbi eget fermentum neque. Quisque et erat ante. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas."
                }
                        ],
                }
        return render(request, 'treninzi.html', context)

class DodavanjeTreningaView(View):
	def get(self, request):
		context = {}
		return render(request, 'dodavanjeTreninga.html', context)
		
	def post(self, request):
		print(request.POST.get('userID'))
		print(request.POST.get('date'))
		print(request.POST.get('startTime'))
		print(request.POST.get('endTime'))
		print(request.POST.get('description'))
		return redirect('/treninzi')
