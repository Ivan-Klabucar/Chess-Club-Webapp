from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponse
from ..models import User, Novost
from datetime import datetime

def render_error(request, message, status_code):
    return render(request, 'error.html', {'err_desc': message}, status=status_code)

class ObjavaNovostiView(View):
    def get(self, request):
        user_curr = request.user
        if not (user_curr.is_superuser or user_curr.is_staff):
            return render_error(request, "Nemate ovlasti za objavu", 400)
        context = {}
        return render(request, 'objavaNovosti.html', context)

    def post(self, request):
        user_curr = request.user
        new_novost = Novost(user = user_curr, vrijemeObjave = datetime.now(), naslov = request.POST.get('title'), tekst = request.POST.get('text'))
        new_novost.save()
        return redirect('/novosti')