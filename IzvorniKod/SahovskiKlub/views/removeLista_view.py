from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponse
from django.contrib.auth.models import User
from SahovskiKlub.models import Profil, Transakcija
from datetime import datetime, date

def render_error(request, message, status_code):
    return render(request, 'error.html', {'err_desc': message}, status=status_code)

class RemoveListView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render_error(request, 'Niste prijavljeni', 400)
        currentuser = Profil.objects.get(user_id=request.user.id)
        if not currentuser.admin:
            return render_error(request, 'Niste admin', 400)

        userList = list(Profil.objects.filter(placenaClanarina=True, zabranjenPristup=False))
        dict = {}

        danasnji_datum = datetime.now()

        if danasnji_datum.strftime("%m") == "01":
            prijasnji_mjesec = 12
        else:
            prijasnji_mjesec = int(danasnji_datum.strftime("%m")) - 1

        zadnji_priznati_dan = danasnji_datum.replace(month=prijasnji_mjesec)
        if(prijasnji_mjesec == 12):
            zadnji_priznati_dan = zadnji_priznati_dan.replace(year=int(danasnji_datum.date().strftime("%Y"))-1)
        for user in userList:
            zadnjaTransakcija = Transakcija.objects.filter(user_id=user.user.id).order_by('-datumTransakcije').first()
            if zadnjaTransakcija is None:
                dict[user] = "Korisnik nema transakciju"
                continue
            if zadnjaTransakcija.datumTransakcije < zadnji_priznati_dan.date():
                dict[user] = zadnjaTransakcija.datumTransakcije

        context = {
            "dictTransakcije": dict
        }
        return render(request, 'removeLista.html', context)

    def post(self, request):
        idNeplacen = int(request.POST.get('status'))
        print(idNeplacen)
        Profil.objects.filter(id=idNeplacen).update(placenaClanarina=False)
        return redirect('/removeLista')
