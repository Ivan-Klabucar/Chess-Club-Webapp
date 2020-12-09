from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse


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
                'new_black_moves': ['d5', 'e5', 'f5', 'fxe4'],
                'opis_greske': "Greska ovdje je ta sto lovac promasi pijuna kojeg zeli pojesti. Zapravo se skroz drukcije to treba sve obaviti. 4/10!"
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
