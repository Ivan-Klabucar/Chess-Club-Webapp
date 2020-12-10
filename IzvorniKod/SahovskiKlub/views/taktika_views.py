from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from SahovskiKlub.models import Taktika, RjesenjeTaktike, DojavaPogreske
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
            'already_solved': vec_rijeseno,
            'taktika_id': taktika.id,
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
        dojava_id = request.GET.get('id', '')
        if not dojava_id:
            return HttpResponse("niste oznacili koju dojavu zelite revidirati", status=400)
        dojava = DojavaPogreske.objects.get(id=dojava_id)
        black_and_white_moves = dojava.predlozeniTijek.split('<W|B>')
        taktika = dojava.taktika
        context = {
            'tactic_data': {
                'revision_id': dojava_id,
                'tactic_id': taktika.id,
                'old_start_position': taktika.initConfig,
                'old_white_moves': taktika.movesWhite.split(','),
                'old_black_moves': taktika.movesBlack.split(','),
                'new_start_position': taktika.initConfig,
                'new_white_moves': black_and_white_moves[0].split(','),
                'new_black_moves': black_and_white_moves[1].split(','),
                'opis_greske': dojava.opis
            }
        }
        return render(request, 'revidiranjeTaktike.html', context)

    def post(self, request):
        confirmed = request.POST.get('confirmed', '')
        revision_id = request.POST.get('revision_id', '')
        if not confirmed or not revision_id:
            return HttpResponse("Nisu poslani svi podatci za potvrdu ili odbacivanje dojave", status=400)
        dojava = DojavaPogreske.objects.get(id=revision_id)
        taktika = dojava.taktika
        black_and_white_moves = dojava.predlozeniTijek.split('<W|B>')
        if confirmed == 'true':
            taktika.movesWhite = black_and_white_moves[0]
            taktika.movesBlack = black_and_white_moves[1]
            dojava.prihvacena = True
            taktika.save()
            dojava.save()
            invalid_solutions = RjesenjeTaktike.objects.filter(taktika_id=taktika.id)
            invalid_solutions.delete()
        else:
            print("rejected")
            dojava.prihvacena = False
            dojava.save()
        return HttpResponse('sve pet')


class TacticErrorReportView(View):
    def get(self, request):
        taktika_id = request.GET.get('id', '')
        if not taktika_id:
            return HttpResponse("niste oznacili na kojoj taktici zelite prijaviti gresku", status=400)
        taktika_id = int(taktika_id)
        taktika = Taktika.objects.get(id=taktika_id)
        context = {
            'revision_data': {
                'start_position': taktika.initConfig,
                'tactic_id': taktika.id
            }
        }
        return render(request, 'dojavaGreske.html', context)

    def post(self, request):
        movesWhite = request.POST.get('white_moves', '')
        movesBlack = request.POST.get('black_moves', '')
        initConfig = request.POST.get('init_config', '')
        errDesc = request.POST.get('error_description', '')
        tactic_id = request.POST.get('tactic_id', '')
        if not movesWhite or not movesBlack or not initConfig or not errDesc or not tactic_id:
            return HttpResponse("niste poslali neki od argumenata", status=400)
        tactic = Taktika.objects.get(id=tactic_id)
        tijek = "{}<W|B>{}".format(movesWhite, movesBlack)
        dojava = DojavaPogreske(taktika=tactic, userDojave=request.user, userRevizija=tactic.user, predlozeniTijek=tijek, opis=errDesc, prihvacena=False)
        dojava.save()
        return HttpResponse("Success")
        
