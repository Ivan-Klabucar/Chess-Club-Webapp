from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse



class TreninziView(View):
    def get(self, request):
        context = {
            "listaTreninga": [
                {
                    "idTreninga": "12",
                    "organizator": "Trener1",
                    "vrijemePocetka": "16:00",
                    "vrijemeZavrsetka": "18:00",
                    "datum": "10.12.2020.",
                    "opis": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc ex metus, dignissim eget mi nec, ullamcorper auctor diam. Donec tincidunt massa quis risus vulputate sollicitudin. Curabitur iaculis mattis tempor. Suspendisse finibus ante sit amet finibus sodales. Proin porttitor fringilla tellus vitae dignissim. Morbi eget massa metus. Proin mollis tellus quis dignissim pulvinar. Nam suscipit nisi mattis nisi euismod consectetur. Sed nec nisl placerat, imperdiet nunc a, ultricies mi. Morbi eget fermentum neque. Quisque et erat ante. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas."
                },
                {
                    "idTreninga": "34",
                    "organizator": "Trener2",
                    "vrijemePocetka": "16:00",
                    "vrijemeZavrsetka": "18:00",
                    "datum": "11.12.2020.",
                    "opis": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc ex metus, dignissim eget mi nec, ullamcorper auctor diam. Donec tincidunt massa quis risus vulputate sollicitudin. Curabitur iaculis mattis tempor. Suspendisse finibus ante sit amet finibus sodales. Proin porttitor fringilla tellus vitae dignissim. Morbi eget massa metus. Proin mollis tellus quis dignissim pulvinar. Nam suscipit nisi mattis nisi euismod consectetur. Sed nec nisl placerat, imperdiet nunc a, ultricies mi. Morbi eget fermentum neque. Quisque et erat ante. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas."
                },
                {
                    "idTreninga": "56",
                    "organizator": "Trener3",
                    "vrijemePocetka": "16:00",
                    "vrijemeZavrsetka": "18:00",
                    "datum": "12.12.2020.",
                    "opis": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc ex metus, dignissim eget mi nec, ullamcorper auctor diam. Donec tincidunt massa quis risus vulputate sollicitudin. Curabitur iaculis mattis tempor. Suspendisse finibus ante sit amet finibus sodales. Proin porttitor fringilla tellus vitae dignissim. Morbi eget massa metus. Proin mollis tellus quis dignissim pulvinar. Nam suscipit nisi mattis nisi euismod consectetur. Sed nec nisl placerat, imperdiet nunc a, ultricies mi. Morbi eget fermentum neque. Quisque et erat ante. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas."
                }
            ],
        }
        return render(request, 'treninzi.html', context)

    def post(self, request):
        print(request.POST.get('idUsera'))
        print(request.POST.get('idTreninga'))
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
