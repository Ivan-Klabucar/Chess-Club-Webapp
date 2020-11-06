from django.shortcuts import render
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login


class HomeView(View):
    def get(self, request):
        return render(request, 'homepage.html')


class RegisterView(View):
    def get(self, request):
        context = {}
        form = UserCreationForm(request.POST or None)
        context['form'] = form
        return render(request, 'registration/sign_up.html', context)

    def post(self, request):
        context = {}
        form = UserCreationForm(request.POST or None)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return render(request, 'homepage.html')
        context['form'] = form
        return render(request, 'registration/sign_up.html', context)