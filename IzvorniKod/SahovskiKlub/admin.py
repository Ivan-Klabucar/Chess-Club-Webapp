from django.contrib import admin
from .models import Profil,Taktika,RjesenjeTaktike,DojavaPogreske,RangLista,Novost,Trening,PrijavaTrening,Turnir,PrijavaTurnir,Transakcija,Aktivnost

# Register your models here.

admin.site.register(Profil)
admin.site.register(Taktika)
admin.site.register(RjesenjeTaktike)
admin.site.register(DojavaPogreske)
admin.site.register(RangLista)
admin.site.register(Novost)
admin.site.register(Trening)
admin.site.register(Turnir)
admin.site.register(PrijavaTrening)
admin.site.register(PrijavaTurnir)
admin.site.register(Transakcija)
admin.site.register(Aktivnost)
