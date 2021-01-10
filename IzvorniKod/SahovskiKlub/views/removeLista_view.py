from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponse
from django.contrib.auth.models import User
from SahovskiKlub.models import Profil, Transakcija

def render_error(request, message, status_code):
    return render(request, 'error.html', {'err_desc': message}, status=status_code)

class RemoveListView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render_error(request, 'Niste prijavljeni', 400)
        currentuser = Profil.objects.get(id=request.user.id)
        if not currentuser.admin:
            return render_error(request, 'Niste admin', 400)

        userList = list(Profil.objects.filter(placenaClanarina=False, zabranjenPristup=False))
        dict = {}
        for user in userList:
            transakcije = Transakcija.objects.filter(user_id=user.id)
            if transakcije is None:
                dict[user] = "Korisnik nema transakciju"
                continue
            zadnjaTransakcija = Transakcija.objects.filter(user_id=user.id).first()
            if zadnjaTransakcija is None:
                dict[user] = "Korisnik nema transakciju"
                continue
            for transakcija in transakcije:
                if transakcija.datumTransakcije.isoformat() > zadnjaTransakcija.datumTransakcije.isoformat():
                    zadnjaTransakcija = transakcija

            dict[user] = zadnjaTransakcija.datumTransakcije

        context = {
            "dictTransakcije": dict
        }
        return render(request, 'removeLista.html', context)

    def post(self, request):
        idNeplacen = int(request.POST.get('status'))
        print(idNeplacen)
        Profil.objects.filter(id=idNeplacen).update(zabranjenPristup=True)
        return redirect('/removeLista')
