from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views import View
from django.http import HttpResponse
from SahovskiKlub.models import User, Turnir, PrijavaTurnir, Aktivnost
from datetime import datetime
from datetime import time
import operator

def render_error(request, message, status_code):
    return render(request, 'error.html', {'err_desc': message}, status=status_code)



class TurniriView(View):
    def get(self, request):
        context = {}
        if(not request.user.profil.trener and not request.user.profil.admin and not request.user.profil.placenaClanarina):
            return render(request, 'placanjeClanarine.html', context)
            a = 0
        turniriNesortirani = Turnir.objects.filter(vidljivost=True)
        turniri = sorted(turniriNesortirani, key=operator.attrgetter('vrijemePocetka'))
        turniriObj = []
        
        for turnir in turniri:
            organizator = User.objects.get(id=turnir.organizator_id)
            prijavljen = False
            svePrijave = PrijavaTurnir.objects.all()
            brojSudionika = 0
            if(svePrijave):
                for prijava in svePrijave:
                    if(prijava.trening_id == turnir.id):
                        brojSudionika = brojSudionika + 1
                        if(prijava.user_id == request.user.id):
                            prijavljen = True

            turnirObj = {  
                            "id": turnir.id,
                            "orgId": organizator.id,
                            "org": organizator.username,
                            "vrijemeP": turnir.vrijemePocetka.strftime("%H:%M"),
                            "vrijemeZ": turnir.vrijemeZavrsetka.strftime("%H:%M"),
                            "datumP": turnir.vrijemePocetka.strftime("%d.%m.%Y"),
                            "datumZ": turnir.vrijemeZavrsetka.strftime("%d.%m.%Y"),
                            "formatTurnira": turnir.formatTurnira,
                            "maxBrojSudionika": turnir.brojSudionika,
                            "brojSudionika": brojSudionika,
                            "prijavljen": prijavljen
                            }
            turniriObj.append(turnirObj)

        context = {
            "listaTurnira": turniriObj
        }
        return render(request, 'turniri.html', context)

    def post(self, request):
        vrstaSubmita = request.POST.get('vrstaSubmita')
        idUser = request.POST.get('idUsera')
        idTurnir = request.POST.get('idTurnira')

        if(vrstaSubmita == "prijava"):
            novaPrijava = PrijavaTurnir(user=User.objects.get(id=idUser), turnir=Turnir.objects.get(id=idTurnir))
            novaAktivnost = Aktivnost(user=request.user, vrijemeAktivnosti=datetime.now(), aktivnost="Prijava na turnir "+idTurnir)
            novaAktivnost.save()
            novaPrijava.save()
        elif(vrstaSubmita == "brisanje"):
            turnirDel = Turnir.objects.get(id=idTurnir)
            turnirDel.vidljivost = False
            novaAktivnost = Aktivnost(user=request.user, vrijemeAktivnosti=datetime.now(), aktivnost="Brisanje turnira "+idTurnir)
            novaAktivnost.save()
            turnirDel.save()
        elif(vrstaSubmita == "odjava"):
            prijavaDel = PrijavaTurnir.objects.get(user_id=idUser, turnir_id=idTurnir)
            novaAktivnost = Aktivnost(user=request.user, vrijemeAktivnosti=datetime.now(), aktivnost="Odjava s turnira "+idTurnir)
            novaAktivnost.save()
            prijavaDel.delete()
        else:
            return render_error(request, "Vrsta formulara ne postoji.", 400)

        return redirect('/turniri')



class DodavanjeTurniraView(View):
    def get(self, request):
        context = {}
        return render(request, 'dodavanjeTurnira.html', context)

    def post(self, request):
        orgId = request.POST.get('orgId')
        vrijemeP = request.POST.get('vrijemeP')
        vrijemeZ = request.POST.get('vrijemeZ')
        formatTurnira = request.POST.get('formatTurnira')
        maxBrojSudionika = request.POST.get('brojSudionika')
        noviTurnir = Turnir(vrijemePocetka=vrijemeP, vrijemeZavrsetka=vrijemeZ, formatTurnira=formatTurnira, brojSudionika=maxBrojSudionika)
        vrijemePocetkaNovi = datetime.strptime(vrijemeP, "%Y-%m-%dT%H:%M")
        vrijemeZavrsetkaNovi = datetime.strptime(vrijemeZ, "%Y-%m-%dT%H:%M")
        sviTurniri = Turnir.objects.filter(vidljivost=True)
        
        brojPreklapanja = 0
        if(len(sviTurniri) > 0):
            for turnir in sviTurniri:
                vrijemePocetkaStari = datetime.strptime(datetime.strftime(turnir.vrijemePocetka, "%Y-%m-%d %H:%M"), "%Y-%m-%d %H:%M")
                vrijemeZavrsetkaStari = datetime.strptime(datetime.strftime(turnir.vrijemeZavrsetka, "%Y-%m-%d %H:%M"), "%Y-%m-%d %H:%M")
                if((vrijemePocetkaStari < vrijemePocetkaNovi < vrijemeZavrsetkaStari) 
                    or (vrijemePocetkaStari < vrijemeZavrsetkaNovi < vrijemeZavrsetkaStari)
                    or (vrijemePocetkaNovi <= vrijemePocetkaStari < vrijemeZavrsetkaStari <= vrijemeZavrsetkaNovi)
                    or (vrijemePocetkaNovi >= vrijemeZavrsetkaNovi)):
                    brojPreklapanja = brojPreklapanja + 1
        if(brojPreklapanja != 0):
            return render_error(request, "Nemoguće stvoriti turnir. Postoji preklapanje s postojećim turnirima ili je vrijeme početka veće od vremena završetka.", 400)
        else:
            noviTurnir.save()
            novaAktivnost = Aktivnost(user=request.user, vrijemeAktivnosti=datetime.now(), aktivnost="Stvaranje turnira "+str(noviTurnir.id))
            novaAktivnost.save()
        return redirect('/turniri')
