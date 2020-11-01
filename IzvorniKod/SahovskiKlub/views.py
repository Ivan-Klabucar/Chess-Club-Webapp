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

def listaTaktika(request):
    context = {
        "listaTaktika" : [
            {
                "autor" : "Marko",
                "datum" : "17.8.2019"
            },
            {
                "autor" : "Ivo",
                "datum" : "19.10.2020"
            }
        ],
        "listaTaktikeIstaknute" : [
            {
                "autor" : "Bruno",
                "datum" : "19.10.2021"
            }
        ]
    }
    return render(request, 'listaDnevnihTaktika.html', context)