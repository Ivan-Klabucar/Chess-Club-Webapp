from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse



class TreninziView(View):
    def get(self, request):
        treninzi = Trening.objects.all()
        listaTreninga = []
        
        for trening in treninzi:
            treningObj = {
                            "org": trening.organizator,
                            "vrijemeP": trening.vrijemePocetka,
                            "vrijemeZ": trening.vrijemeZavrsetka,
                            "opis": trening.opisTreninga
                            }
            treninziObj.append(treningObj)
        
        
        context = {
            "listaTreninga": treninziObj
        }
        return render(request, 'treninzi.html', context)

    def post(self, request):
        idUser = request.POST.get('idUsera')
        idTrening = request.POST.get('idTreninga')
        prijava = PrijavaTrening(user=idUser, trening=idTrening)
        prijava.save()
        return redirect('/treninzi')



class DodavanjeTreningaView(View):
    def get(self, request):
        context = {}
        return render(request, 'dodavanjeTreninga.html', context)

    def post(self, request):
        print(request.POST.get('userID'))
        print(request.POST.get('date'))
        print(request.POST.get('startTime'))
        print(request.POST.get('endTime'))
        print(request.POST.get('description'))
        return redirect('/treninzi')
