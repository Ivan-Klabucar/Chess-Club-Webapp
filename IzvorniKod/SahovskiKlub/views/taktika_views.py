from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from SahovskiKlub.models import Taktika, RjesenjeTaktike
from datetime import datetime
from django.core import serializers


class TacticView(View):
    def get(self, request):
        taktika_id = request.GET.get('id', '')
        if not taktika_id:
            return HttpResponse("niste oznacili koju taktiku zelite rjesiti", status=400)
        vec_rijeseno = False
        taktika_id = int(taktika_id)
        proslost_rjesavanja = RjesenjeTaktike.objects.filter(taktika_id=taktika_id, user_id=request.user.id)
        if proslost_rjesavanja: vec_rijeseno = True
        taktika = Taktika.objects.get(id=taktika_id)
        serialized_taktika = serializers.serialize('json', [taktika])
        print(serialized_taktika)
        context = {
            'tactic_data': serialized_taktika,
            'tezina': taktika.tezina,
            'already_solved': vec_rijeseno
        }
        return render(request, 'taktika.html', context)

    def post(self, request):
        sekunde = request.POST.get('sekunde', '')
        taktika_id = request.POST.get('taktika_id', '')
        glas_tezina = request.POST.get('tezina', '')
        if not sekunde or not taktika_id:
            return HttpResponse("Krivi argumenti za rjesenje taktike", status=400)
        taktika = Taktika.objects.get(id=taktika_id)
        proslost_rjesavanja = RjesenjeTaktike.objects.filter(taktika_id=taktika_id, user_id=request.user.id)
        if not proslost_rjesavanja:
            rjesenje = RjesenjeTaktike(user=request.user, taktika=taktika, vrijeme=float(sekunde))
            rjesenje.save()

            if glas_tezina:
                nova_tezina = ((taktika.tezina * taktika.brojGlasova) + int(glas_tezina)) / (taktika.brojGlasova + 1)
                taktika.brojGlasova = taktika.brojGlasova + 1
                taktika.tezina = nova_tezina
                taktika.save()
        return HttpResponse("Success")


class TacticCreationView(View):
    def get(self, request):
        context = {}
        return render(request, 'objavaTaktike.html', context)

    def post(self, request):
        init_config = request.POST.get('init_config', '')
        white_moves = request.POST.get('white_moves', '')
        black_moves = request.POST.get('black_moves', '')
        tezina = request.POST.get('tezina', '')
        curr_user = request.user
        if not init_config or not white_moves or not black_moves or not tezina or not curr_user:
            return HttpResponse("krivo zadana taktika", status=500)

        new_tactic = Taktika(user=curr_user, initConfig=init_config,
                             movesWhite=white_moves, movesBlack=black_moves, tezina=int(tezina), brojGlasova=1, createdAt=datetime.now())
        new_tactic.save()
        return redirect('/objavaTaktike')


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
