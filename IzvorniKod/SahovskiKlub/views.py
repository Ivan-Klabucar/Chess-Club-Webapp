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
                    "zadnjaTransakcija" : "11.2020."
                },
                {
                    "ime": "Ivo",
                    "zadnjaTransakcija" : "10.2020."
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
        print()
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
            print("Revision #{} was confirmed".format(
                request.POST.get('id', '')))
        else:
            print("Revision #{} was rejected".format(
                request.POST.get('id', '')))
        return HttpResponse('sve pet')


class TreninziView(View):
    def get(self, request):
        context = {
            "listaTreninga": [
                {
                    "idTreninga": "12",
                    "organizator": "Trener1",
                    "vrijemePocetka": "16:00",
                    "vrijemeZavrsetka": "18:00",
                    "datum": "10.12.2020.",
                    "opis": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc ex metus, dignissim eget mi nec, ullamcorper auctor diam. Donec tincidunt massa quis risus vulputate sollicitudin. Curabitur iaculis mattis tempor. Suspendisse finibus ante sit amet finibus sodales. Proin porttitor fringilla tellus vitae dignissim. Morbi eget massa metus. Proin mollis tellus quis dignissim pulvinar. Nam suscipit nisi mattis nisi euismod consectetur. Sed nec nisl placerat, imperdiet nunc a, ultricies mi. Morbi eget fermentum neque. Quisque et erat ante. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas."
                },
                {
                    "idTreninga": "34",
                    "organizator": "Trener2",
                    "vrijemePocetka": "16:00",
                    "vrijemeZavrsetka": "18:00",
                    "datum": "11.12.2020.",
                    "opis": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc ex metus, dignissim eget mi nec, ullamcorper auctor diam. Donec tincidunt massa quis risus vulputate sollicitudin. Curabitur iaculis mattis tempor. Suspendisse finibus ante sit amet finibus sodales. Proin porttitor fringilla tellus vitae dignissim. Morbi eget massa metus. Proin mollis tellus quis dignissim pulvinar. Nam suscipit nisi mattis nisi euismod consectetur. Sed nec nisl placerat, imperdiet nunc a, ultricies mi. Morbi eget fermentum neque. Quisque et erat ante. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas."
                },
                {
                    "idTreninga": "56",
                    "organizator": "Trener3",
                    "vrijemePocetka": "16:00",
                    "vrijemeZavrsetka": "18:00",
                    "datum": "12.12.2020.",
                    "opis": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc ex metus, dignissim eget mi nec, ullamcorper auctor diam. Donec tincidunt massa quis risus vulputate sollicitudin. Curabitur iaculis mattis tempor. Suspendisse finibus ante sit amet finibus sodales. Proin porttitor fringilla tellus vitae dignissim. Morbi eget massa metus. Proin mollis tellus quis dignissim pulvinar. Nam suscipit nisi mattis nisi euismod consectetur. Sed nec nisl placerat, imperdiet nunc a, ultricies mi. Morbi eget fermentum neque. Quisque et erat ante. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas."
                }
            ],
        }
        return render(request, 'treninzi.html', context)

    def post(self, request):
        print(request.POST.get('idUsera'))
        print(request.POST.get('idTreninga'))
        return redirect('/treninzi')


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


class TurniriView(View):
    def get(self, request):
        context = {
            "listaTurnira": [
                {
                    "idTurnira": "343453",
                    "organizator": "Trener1",
                    "vrijemePocetka": "21.12.2020. 10:00",
                    "vrijemeZavrsetka": "23.12.2020. 18:00",
                    "brojSudionika": "32",
                    "formatTurnira": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc ex metus, dignissim eget mi nec, ullamcorper auctor diam. Donec tincidunt massa quis risus vulputate sollicitudin. Curabitur iaculis mattis tempor. Suspendisse finibus ante sit amet finibus sodales. Proin porttitor fringilla tellus vitae dignissim. Morbi eget massa metus. Proin mollis tellus quis dignissim pulvinar. Nam suscipit nisi mattis nisi euismod consectetur. Sed nec nisl placerat, imperdiet nunc a, ultricies mi. Morbi eget fermentum neque. Quisque et erat ante. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas."
                },
                {
                    "idTurnira": "785654",
                    "organizator": "Trener2",
                    "vrijemePocetka": "21.1.2021. 10:00",
                    "vrijemeZavrsetka": "23.1.2021. 18:00",
                    "brojSudionika": "32",
                    "formatTurnira": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc ex metus, dignissim eget mi nec, ullamcorper auctor diam. Donec tincidunt massa quis risus vulputate sollicitudin. Curabitur iaculis mattis tempor. Suspendisse finibus ante sit amet finibus sodales. Proin porttitor fringilla tellus vitae dignissim. Morbi eget massa metus. Proin mollis tellus quis dignissim pulvinar. Nam suscipit nisi mattis nisi euismod consectetur. Sed nec nisl placerat, imperdiet nunc a, ultricies mi. Morbi eget fermentum neque. Quisque et erat ante. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas."
                },
                {
                    "idTurnira": "24321",
                    "organizator": "Admin",
                    "vrijemePocetka": "21.2.2021. 10:00",
                    "vrijemeZavrsetka": "23.2.2021. 18:00",
                    "brojSudionika": "32",
                    "formatTurnira": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc ex metus, dignissim eget mi nec, ullamcorper auctor diam. Donec tincidunt massa quis risus vulputate sollicitudin. Curabitur iaculis mattis tempor. Suspendisse finibus ante sit amet finibus sodales. Proin porttitor fringilla tellus vitae dignissim. Morbi eget massa metus. Proin mollis tellus quis dignissim pulvinar. Nam suscipit nisi mattis nisi euismod consectetur. Sed nec nisl placerat, imperdiet nunc a, ultricies mi. Morbi eget fermentum neque. Quisque et erat ante. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas."
                }
            ],
        }
        return render(request, 'turniri.html', context)

    def post(self, request):
        print(request.POST.get('idUsera'))
        print(request.POST.get('idTurnira'))
        return redirect('/turniri')


class TacticErrorReportView(View):
    def get(self, request):
        current_tactic = {
            'id': 74,
            'start_position': 'rnbqkbnr/pppppppp/8/8/7P/8/PPPPPPPB/RNBQK1NR w KQkq - 0 1',
            'white_moves': ['d4', 'e4', 'f4', 'exd5', 'Bcxf4'],
            'black_moves': ['d5', 'e5', 'f5', 'exf4'],
        }
        context = {
            'revision_data': {
                'start_position': current_tactic['start_position']
            }
        }
        return render(request, 'dojavaGreske.html', context)

    def post(self, request):
        print("bijeli potezi:")
        print(request.POST.get('white_moves', ''))
        print("crni potezi:")
        print(request.POST.get('black_moves', ''))
        print("init config:")
        print(request.POST.get('init_config', ''))
        print("error desc:")
        print(request.POST.get('error_description', ''))
        return HttpResponse('sve pet')


class ObjavaNovostiView(View):
    def get(self, request):
        context = {}
        return render(request, 'objavaNovosti.html', context)

    def post(self, request):
        print(request.POST.get('title'))
        print(request.POST.get('text'))
        return redirect('/novosti')


class DodavanjeTurniraView(View):
    def get(self, request):
        context = {}
        return render(request, 'dodavanjeTurnira.html', context)

    def post(self, request):
        print(request.POST.get('userID'))
        print(request.POST.get('vrijemePocetka'))
        print(request.POST.get('vrijemeZavrsetka'))
        print(request.POST.get('brojSudionika'))
        print(request.POST.get('formatTurnira'))
        return redirect('/turniri')
