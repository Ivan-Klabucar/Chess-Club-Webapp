from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.views import View
from django.http import HttpResponse, HttpResponseForbidden
from SahovskiKlub.models import User, Taktika, DojavaPogreske
from datetime import datetime
from datetime import time
import operator

def render_error(request, message, status_code):
    return render(request, 'error.html', {'err_desc': message}, status=status_code)



class DojavaPogreskiView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render_error(request, 'Samo treneri i admini imaju pristup listi dojava pogreški', 400)
        context = {}
        if request.user.profil.zabranjenPristup:
            return HttpResponseForbidden()
        if not request.user.profil.trener or request.user.profil.admin:
            return render_error(request, 'Samo treneri i admini imaju pristup listi dojava pogreški', 400)
        dojave = DojavaPogreske.objects.filter(userRevizija=request.user, prihvacena__isnull=True)
        dojaveObj = []
        
        for dojava in dojave:
            recenzent = dojava.userRevizija
            taktika = dojava.taktika

            dojavaObj = {   
                            "id": dojava.id,
                            "imeTaktike": taktika.ime,
                            "posiljatelj": dojava.userDojave,
                            "opis": dojava.opis
                            }
            dojaveObj.append(dojavaObj)

        context = {
            "listaDojava": dojaveObj
        }
        return render(request, 'listaDojavaPogreski.html', context)

    def post(self, request):
        idDojave = request.POST.get('idDojave')
        return redirect('/revidiranjeTaktike?id=' + idDojave)
