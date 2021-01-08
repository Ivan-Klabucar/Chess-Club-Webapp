from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from ..models import *
from datetime import datetime

def render_error(request, message, status_code):
    return render(request, 'error.html', {'err_desc': message}, status=status_code)

class SviProfiliView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render_error(request, 'Niste prijavljeni', 400)
        currentuser = Profil.objects.get(user_id=request.user.id)
        if currentuser.zabranjenPristup:
            return render_error(request, 'Zabranjen pristup', 400)
        if not currentuser.admin:
            return render_error(request, 'Morate biti admin kako biste pristupili listi profila', 400)

        userList = list(Profil.objects.all().order_by('user_id'))
        context = {
            "users": userList
        }

        return render(request, 'sviProfili.html', context)

class DetaljanProfilView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return render_error(request, 'Niste prijavljeni', 400)
        currentuser = Profil.objects.get(user_id=request.user.id)
        if currentuser.zabranjenPristup:
            return render_error(request, 'Zabranjen pristup', 400)
        if not currentuser.admin:
            return render_error(request, 'Morate biti admin kako biste pristupili prikazu profila', 400)

        detaljan_id = request.GET.get('id', '')
        if not detaljan_id:
            return render_error(request, 'Niste odabrali profil za detaljan prikaz', 400)
        if not Profil.objects.filter(user_id=detaljan_id).exists():
            return render_error(request, 'Profil s zadanim id-om ne postoji', 400)
        user = Profil.objects.get(user_id=detaljan_id)
        activityList = list(Aktivnost.objects.filter(user_id=detaljan_id).order_by('vrijemeAktivnosti'))
        context = {
            "detaljan_user": user,
            "listaAktivnosti": activityList
        }
        return render(request, 'detaljanProfil.html', context)

    def post(self, request):
        if request.POST.get('enable'):
            detaljan_id = request.POST.get('enable')
            Profil.objects.filter(user_id=detaljan_id).update(zabranjenPristup=False)
        elif request.POST.get('disable'):
            detaljan_id = request.POST.get('disable')
            Profil.objects.filter(user_id=detaljan_id).update(zabranjenPristup=True)
        return redirect('/detaljanProfil?id=' + detaljan_id)



