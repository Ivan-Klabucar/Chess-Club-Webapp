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
        currentuser = Profil.objects.get(id=request.user.id)
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
        currentuser = Profil.objects.get(id=request.user.id)
        if currentuser.zabranjenPristup:
            return render_error(request, 'Zabranjen pristup', 400)
        if not currentuser.admin:
            return render_error(request, 'Morate biti admin kako biste pristupili prikazu profila', 400)

        user_id = request.GET.get('id', '')
        if not user_id:
            return render_error(request, 'Niste odabrali profil za detaljan prikaz', 400)
        if not Profil.objects.filter(id=user_id).exists():
            return render_error(request, 'Profil s zadanim id-om ne postoji', 400)
        user = Profil.objects.get(id=user_id)
        context = {
            "detaljan_user": user
        }
        return render(request, 'detaljanProfil.html', context)

    def post(self, request):
        if request.POST.get('enable'):
            user_id = request.POST.get('enable')
            Profil.objects.filter(id=user_id).update(zabranjenPristup=False)
        elif request.POST.get('disable'):
            user_id = request.POST.get('disable')
            Profil.objects.filter(id=user_id).update(zabranjenPristup=True)
        return redirect('/detaljanProfil?id=' + user_id)



