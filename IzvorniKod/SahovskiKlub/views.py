from django.shortcuts import render
from django.views import View

from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login

# Create your views here

class HomeView(View):
    def get(self, request):
        return render(request, 'homepage.html')

def sign_up(request):
    context = {}
    form = UserCrseationForm(request.POST or None)
    if request.method == "POST":
        if form.is_valid():
            user = form.save()
            login(request, user)
            return render(request, 'homepage.html')
    context['form'] = form
    return render(request, 'registration/sign_up.html', context)

def novosti(request):
    context = {
        "listaNovosti" : [
            {
                "naslov" : "test",
                "korisnik" : "Marko",
                "datum" : "30.10.2020",
                "opis" : "Tu smo se prikupili kako bismo ispratili našu dragu volju u bolji život. Oduvijek smo znali da je ona pre dobra za ovaj život, te da je neljudski ju držati ovdje"
            },
            {
                "naslov" : "test2",
                "korsinik" : "Ivo",
                "datum" : "31.10.2020",
                "opis" : "Marko nam je svima lagao, on je lažni mesija. Čujte i počujte, o narode, jer ja vam kažem, uredu je. Zašto? Jer sam ja došao!"
            }
        ]
    }
    return render(request, 'novosti/novosti.html', context)