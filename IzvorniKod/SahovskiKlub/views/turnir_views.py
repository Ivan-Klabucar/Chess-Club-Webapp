from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse



class TurniriView(View):
    def get(self, request):
        context = {
            "listaTurnira": [
                {
                    "idTurnira": "343453",
                    "organizator": "Trener1",
                    "vrijemePocetka": "21.12.2020. 10:00",
                    "vrijemeZavrsetka": "23.12.2020. 18:00",
                    "brojSudionika": "32",
                    "formatTurnira": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc ex metus, dignissim eget mi nec, ullamcorper auctor diam. Donec tincidunt massa quis risus vulputate sollicitudin. Curabitur iaculis mattis tempor. Suspendisse finibus ante sit amet finibus sodales. Proin porttitor fringilla tellus vitae dignissim. Morbi eget massa metus. Proin mollis tellus quis dignissim pulvinar. Nam suscipit nisi mattis nisi euismod consectetur. Sed nec nisl placerat, imperdiet nunc a, ultricies mi. Morbi eget fermentum neque. Quisque et erat ante. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas."
                },
                {
                    "idTurnira": "785654",
                    "organizator": "Trener2",
                    "vrijemePocetka": "21.1.2021. 10:00",
                    "vrijemeZavrsetka": "23.1.2021. 18:00",
                    "brojSudionika": "32",
                    "formatTurnira": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc ex metus, dignissim eget mi nec, ullamcorper auctor diam. Donec tincidunt massa quis risus vulputate sollicitudin. Curabitur iaculis mattis tempor. Suspendisse finibus ante sit amet finibus sodales. Proin porttitor fringilla tellus vitae dignissim. Morbi eget massa metus. Proin mollis tellus quis dignissim pulvinar. Nam suscipit nisi mattis nisi euismod consectetur. Sed nec nisl placerat, imperdiet nunc a, ultricies mi. Morbi eget fermentum neque. Quisque et erat ante. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas."
                },
                {
                    "idTurnira": "24321",
                    "organizator": "Admin",
                    "vrijemePocetka": "21.2.2021. 10:00",
                    "vrijemeZavrsetka": "23.2.2021. 18:00",
                    "brojSudionika": "32",
                    "formatTurnira": "Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nunc ex metus, dignissim eget mi nec, ullamcorper auctor diam. Donec tincidunt massa quis risus vulputate sollicitudin. Curabitur iaculis mattis tempor. Suspendisse finibus ante sit amet finibus sodales. Proin porttitor fringilla tellus vitae dignissim. Morbi eget massa metus. Proin mollis tellus quis dignissim pulvinar. Nam suscipit nisi mattis nisi euismod consectetur. Sed nec nisl placerat, imperdiet nunc a, ultricies mi. Morbi eget fermentum neque. Quisque et erat ante. Pellentesque habitant morbi tristique senectus et netus et malesuada fames ac turpis egestas."
                }
            ],
        }
        return render(request, 'turniri.html', context)

    def post(self, request):
        print(request.POST.get('idUsera'))
        print(request.POST.get('idTurnira'))
        return redirect('/turniri')



class DodavanjeTurniraView(View):
    def get(self, request):
        context = {}
        return render(request, 'dodavanjeTurnira.html', context)

    def post(self, request):
        print(request.POST.get('userID'))
        print(request.POST.get('vrijemePocetka'))
        print(request.POST.get('vrijemeZavrsetka'))
        print(request.POST.get('brojSudionika'))
        print(request.POST.get('formatTurnira'))
        return redirect('/turniri')
        
        
        