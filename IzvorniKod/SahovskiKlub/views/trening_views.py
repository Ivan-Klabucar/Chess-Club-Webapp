from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views import View
from django.http import HttpResponse, HttpResponseForbidden
from SahovskiKlub.models import User, Trening, PrijavaTrening, Aktivnost
from datetime import datetime
from datetime import time
import operator


def render_error(request, message, status_code):
    return render(request, 'error.html', {'err_desc': message}, status=status_code)



class TreninziView(View):
    def get(self, request):
        context = {}
        if request.user.profil.zabranjenPristup:
            return HttpResponseForbidden()
        if(not request.user.profil.trener and not request.user.profil.admin and not request.user.profil.placenaClanarina):
            return redirect('/placanjeClanarine')
            a = 0
        treninziNesortirani = Trening.objects.filter(vidljivost=True)
        treninzi = sorted(treninziNesortirani, key=operator.attrgetter('vrijemePocetka'))
        treninziObj = []
        
        for trening in treninzi:
            organizator = User.objects.get(id=trening.organizator_id)
            prijavljen = False
            svePrijave = PrijavaTrening.objects.all()
            
            if(svePrijave):
                for prijava in svePrijave:
                    if(prijava.user_id == request.user.id and prijava.trening_id == trening.id):
                        prijavljen = True
                        
            treningObj = {  
                            "id": trening.id,
                            "orgId": organizator.id,
                            "org": organizator.username,
                            "vrijemeP": trening.vrijemePocetka.strftime("%H:%M"),
                            "vrijemeZ": trening.vrijemeZavrsetka.strftime("%H:%M"),
                            "datum": trening.vrijemePocetka.strftime("%d.%m.%Y"),
                            "opis": trening.opisTreninga,
                            "prijavljen": prijavljen
                            }
            treninziObj.append(treningObj)
        
        context = {
            "listaTreninga": treninziObj
        }
        return render(request, 'treninzi.html', context)

    def post(self, request):
        vrstaSubmita = request.POST.get('vrstaSubmita')
        idUser = request.POST.get('idUsera')
        idTrening = request.POST.get('idTreninga')

        if(vrstaSubmita == "prijava"):
            novaPrijava = PrijavaTrening(user=User.objects.get(id=idUser), trening=Trening.objects.get(id=idTrening))
            novaAktivnost = Aktivnost(user=request.user, vrijemeAktivnosti=datetime.now(), aktivnost="Prijava na trening "+idTrening)
            novaAktivnost.save()
            novaPrijava.save()
        elif(vrstaSubmita == "brisanje"):
            treningDel = Trening.objects.get(id=idTrening)
            treningDel.vidljivost = False
            novaAktivnost = Aktivnost(user=request.user, vrijemeAktivnosti=datetime.now(), aktivnost="Brisanje treninga "+idTrening)
            novaAktivnost.save()
            treningDel.save()
        elif(vrstaSubmita == "odjava"):
            prijavaDel = PrijavaTrening.objects.get(user_id=idUser, trening_id=idTrening)
            novaAktivnost = Aktivnost(user=request.user, vrijemeAktivnosti=datetime.now(), aktivnost="Odjava s treninga "+idTrening)
            novaAktivnost.save()
            prijavaDel.delete()
        else:
            return render_error(request, "Vrsta formulara ne postoji.", 400)

        return redirect('/treninzi')



class DodavanjeTreningaView(View):
    def get(self, request):
        context = {}
        user = request.user
        if request.user.profil.zabranjenPristup:
            return HttpResponseForbidden()
        if not (user.is_superuser or user.is_staff):
            return render_error(request, "Nemate ovlasti za stvaranje treninga.", 400)
        else:
            return render(request, 'dodavanjeTreninga.html', context)

    def post(self, request):
        orgId = request.POST.get('orgId')
        vrijemeP = request.POST.get('vrijemeP')
        vrijemeZ = request.POST.get('vrijemeZ')
        opis = request.POST.get('opis')
        noviTrening = Trening(organizator_id=orgId, vrijemePocetka=vrijemeP, vrijemeZavrsetka=vrijemeZ, opisTreninga=opis)
        vrijemePocetkaNovi = datetime.strptime(vrijemeP, "%Y-%m-%dT%H:%M")
        vrijemeZavrsetkaNovi = datetime.strptime(vrijemeZ, "%Y-%m-%dT%H:%M")
        sviTreninzi = Trening.objects.filter(vidljivost=True)
        
        brojPreklapanja = 0
        if(len(sviTreninzi) > 0):
            for trening in sviTreninzi:
                vrijemePocetkaStari = datetime.strptime(datetime.strftime(trening.vrijemePocetka, "%Y-%m-%d %H:%M"), "%Y-%m-%d %H:%M")
                vrijemeZavrsetkaStari = datetime.strptime(datetime.strftime(trening.vrijemeZavrsetka, "%Y-%m-%d %H:%M"), "%Y-%m-%d %H:%M")
                if((vrijemePocetkaStari < vrijemePocetkaNovi < vrijemeZavrsetkaStari) 
                    or (vrijemePocetkaStari < vrijemeZavrsetkaNovi < vrijemeZavrsetkaStari)
                    or (vrijemePocetkaNovi <= vrijemePocetkaStari < vrijemeZavrsetkaStari <= vrijemeZavrsetkaNovi)
                    or (vrijemePocetkaNovi >= vrijemeZavrsetkaNovi)):
                    brojPreklapanja = brojPreklapanja + 1
        if(brojPreklapanja != 0):
            return render_error(request, "Nemoguće stvoriti trening. Postoji preklapanje s postojećim treninzima ili je vrijeme početka veće od vremena završetka.", 400)
        else:
            noviTrening.save()
            novaAktivnost = Aktivnost(user=request.user, vrijemeAktivnosti=datetime.now(), aktivnost="Stvaranje treninga "+str(noviTrening.id))
            novaAktivnost.save()
        return redirect('/treninzi')
