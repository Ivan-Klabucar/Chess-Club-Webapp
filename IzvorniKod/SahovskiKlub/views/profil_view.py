from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponse, HttpResponseForbidden
from django.contrib.auth.models import User
from SahovskiKlub.models import Aktivnost, PrijavaTrening, PrijavaTurnir, Profil

def render_error(request, message, status_code):
    return render(request, 'error.html', {'err_desc': message}, status=status_code)

class ProfileView(View):
    def get(self, request):
        if request.user.profil.zabranjenPristup:
            return HttpResponseForbidden()
        if not request.user.is_authenticated:
            return render_error(request, 'Niste prijavljeni', 400)
        user = Profil.objects.get(user_id=request.user.id)
        if user.admin:
            role = "Admin"
        elif user.trener:
            role = "Trener"
        else:
            role = "Član kluba"

        activityList = list(Aktivnost.objects.filter(user_id=request.user.id).order_by('vrijemeAktivnosti'))

        treningApplications = list(
            PrijavaTrening.objects.filter(user_id=request.user.id).order_by('trening__vrijemePocetka'))
        turnirApplications = list(
            PrijavaTurnir.objects.filter(user_id=request.user.id).order_by('turnir__vrijemePocetka'))

        context = {
            "uloga": role,
            "listaAktivnosti": activityList,
            "prijaveTrening": treningApplications,
            "prijaveTurnir": turnirApplications
        }
        return render(request, 'profil.html', context)

    def post(self, request):
        if request.POST.get('odjavaTrening'):
            idTreninga = int(request.POST.get('odjavaTrening'))
            PrijavaTrening.objects.filter(id=idTreninga).delete()
        elif request.POST.get('odjavaTurnir'):
            idTurnira = int(request.POST.get('odjavaTurnir'))
            PrijavaTurnir.objects.filter(id=idTurnira).delete()
        return redirect('/profil')