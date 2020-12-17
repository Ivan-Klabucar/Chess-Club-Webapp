from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from SahovskiKlub.models import Taktika, RjesenjeTaktike, DojavaPogreske, Aktivnost
from datetime import datetime
from django.core import serializers

def render_error(request, message, status_code):
    return render(request, 'error.html', {'err_desc': message}, status=status_code)

def valid_moves(white_moves, black_moves):
    white_moves = white_moves.split(',')
    if black_moves == '': 
        black_moves = []
    else:
        black_moves = black_moves.split(',')
    if len(white_moves) == len(black_moves) + 1:
        return True
    else:
        return False

def log_activity(user, description):
    new_activity = Aktivnost(user=user, aktivnost=description, vrijemeAktivnosti=datetime.now())
    new_activity.save()

class TacticView(View):
    def get(self, request):
        taktika_id = request.GET.get('id', '')
        if not taktika_id:
            return render_error(request, 'Niste označili koju taktiku želite rješiti', 400)
        
        vec_rijeseno = False
        taktika_id = int(taktika_id)
        proslost_rjesavanja = RjesenjeTaktike.objects.filter(taktika_id=taktika_id, user_id=request.user.id)
        if proslost_rjesavanja: vec_rijeseno = True
        taktika = Taktika.objects.get(id=taktika_id)
        serialized_taktika = serializers.serialize('json', [taktika])
        context = {
            'tactic_data': serialized_taktika,
            'tezina': taktika.tezina,
            'already_solved': vec_rijeseno,
            'taktika_id': taktika.id,
        }
        return render(request, 'taktika.html', context)

    def post(self, request):
        if not request.user.is_authenticated:
            return render_error(request, 'Morate se prijaviti kako bi evidentirali rješenja taktike', 400)
        if request.user.profil.admin or request.user.profil.trener:
            return render_error(request, 'Treneri i admini se ne mogu natjecati u rješavanju dnevnih taktika', 400)
        
        sekunde = request.POST.get('sekunde', '')
        taktika_id = request.POST.get('taktika_id', '')
        glas_tezina = request.POST.get('tezina', '')
        if not sekunde or not taktika_id:
            return render_error(request, 'Krivi argumenti za rješenje taktike', 400)
        
        taktika = Taktika.objects.get(id=taktika_id)
        proslost_rjesavanja = RjesenjeTaktike.objects.filter(taktika_id=taktika_id, user_id=request.user.id)
        if not proslost_rjesavanja:
            rjesenje = RjesenjeTaktike(user=request.user, taktika=taktika, vrijeme=float(sekunde))
            rjesenje.save()
            log_activity(request.user, "Rješena taktika #{}, {}".format(taktika.id, taktika.ime))

            if glas_tezina:
                nova_tezina = ((taktika.tezina * taktika.brojGlasova) + int(glas_tezina)) / (taktika.brojGlasova + 1)
                taktika.brojGlasova = taktika.brojGlasova + 1
                taktika.tezina = nova_tezina
                taktika.save()
                log_activity(request.user, "Glasanje za težinu taktike #{}, glasana težina: {}".format(taktika.id, glas_tezina))
        return HttpResponse("Success")


class TacticCreationView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render_error(request, 'Niste prijavljeni', 400)
        if not request.user.profil.trener and not request.user.profil.admin:
            return render_error(request, 'Morate biti trener ili admin da biste objavljivali taktike', 400)
        context = {}
        return render(request, 'objavaTaktike.html', context)

    def post(self, request):
        if not request.user.is_authenticated:
            return render_error(request, 'Niste prijavljeni', 400)
        if not request.user.profil.trener and not request.user.profil.admin:
            return render_error(request, 'Morate biti trener ili admin da biste objavljivali taktike', 400)
        
        init_config = request.POST.get('init_config', '')
        white_moves = request.POST.get('white_moves', '')
        black_moves = request.POST.get('black_moves', '')
        tezina = request.POST.get('tezina', '')
        tactic_name = request.POST.get('tactic_name', '')
        curr_user = request.user
        if not tactic_name or not init_config or not white_moves or not tezina or not curr_user or not valid_moves(white_moves, black_moves):
            return render_error(request, 'Krivo zadana taktika', 400)

        new_tactic = Taktika(user=curr_user, initConfig=init_config,
                             movesWhite=white_moves, movesBlack=black_moves, tezina=int(tezina), brojGlasova=1, createdAt=datetime.now(), ime=tactic_name)
        new_tactic.save()
        log_activity(request.user, "Kreirana taktika #{}, {}".format(new_tactic.id, new_tactic.ime))
        return redirect('/objavaTaktike')


class TacticRevisionView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render_error(request, 'Niste prijavljeni', 400)
        if not request.user.profil.trener and not request.user.profil.admin:
            return render_error(request, 'Morate biti trener ili admin da biste revidirali taktike', 400)

        dojava_id = request.GET.get('id', '')
        if not dojava_id:
            return render_error(request, 'Niste označili koju dojavu želite pregledati', 400)
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
        if not request.user.is_authenticated:
            return render_error(request, 'Niste prijavljeni', 400)
        if not request.user.profil.trener and not request.user.profil.admin:
            return render_error(request, 'Morate biti trener ili admin da biste revidirali taktike', 400)

        confirmed = request.POST.get('confirmed', '')
        revision_id = request.POST.get('revision_id', '')
        if not confirmed or not revision_id:
            return render_error(request, 'Nepotpuni podatci.', 400)
        
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
            log_activity(request.user, "Prihvaćena dojava o grešci #{}".format(dojava.id))
        else:
            dojava.prihvacena = False
            dojava.save()
            log_activity(request.user, "Odbijena dojava o grešci #{}".format(dojava.id))
        return HttpResponse('sve pet')


class TacticErrorReportView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render_error(request, 'Niste prijavljeni', 400)

        taktika_id = request.GET.get('id', '')
        if not taktika_id:
            return render_error(request, 'Niste označili na kojoj taktici želite prijaviti grešku', 400)
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
        if not request.user.is_authenticated:
            return render_error(request, 'Niste prijavljeni', 400)

        movesWhite = request.POST.get('white_moves', '')
        movesBlack = request.POST.get('black_moves', '')
        initConfig = request.POST.get('init_config', '')
        errDesc = request.POST.get('error_description', '')
        tactic_id = request.POST.get('tactic_id', '')
        if not movesWhite or not initConfig or not errDesc or not tactic_id or not valid_moves(movesWhite, movesBlack):
            return render_error(request, 'Nisu poslani svi argumenti', 400)
        tactic = Taktika.objects.get(id=tactic_id)
        tijek = "{}<W|B>{}".format(movesWhite, movesBlack)
        dojava = DojavaPogreske(taktika=tactic, userDojave=request.user, userRevizija=tactic.user, predlozeniTijek=tijek, opis=errDesc)
        dojava.save()
        log_activity(request.user, "Dojavljena greška u taktici #{}, id dojave: {}".format(tactic.id, dojava.id))
        return HttpResponse("Success")
        
