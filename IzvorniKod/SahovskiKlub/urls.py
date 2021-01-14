from django.urls import path
from django.contrib.auth import views
from .views import HomeView, RegisterView, PregledTransakcijaView, RemoveListView, ProfileView
from .views import TreninziView, DodavanjeTreningaView, TurniriView, DodavanjeTurniraView
from .views import ListaTaktikaView, ObrisiTaktikuView
from .views import ProfileView
from .views import RemoveListView
from .views import PregledTransakcijaView, ZabraniPristupView
from .views import TacticView, TacticCreationView, TacticRevisionView, TacticErrorReportView
from .views.objavaNovosti_view import ObjavaNovostiView
from .views.placanjeClanarine_view import PlacanjeClanarineView
from .views.sviProfili_view import SviProfiliView, DetaljanProfilView
from .views.prikazNovosti_view import NovostiView
from .views import TacticView, TacticCreationView, TacticRevisionView, TacticErrorReportView, ListaTaktikaView, RangListaView
from .views.dojavaPogreski_views import DojavaPogreskiView

urlpatterns = [
    path('', HomeView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('login', views.LoginView.as_view()),
    path('register', RegisterView.as_view()),
    path('dnevneTaktike', ListaTaktikaView.as_view()),
    path('taktika', TacticView.as_view()),
    path('objavaTaktike', TacticCreationView.as_view()),
    path('revidiranjeTaktike', TacticRevisionView.as_view()),
    path('novosti', NovostiView.as_view()),
    path('objavaNovosti', ObjavaNovostiView.as_view()),
    path('profil', ProfileView.as_view()),
    path('treninzi', TreninziView.as_view()),
    path('dodavanjeTreninga', DodavanjeTreningaView.as_view()),
    path('turniri', TurniriView.as_view()),
    path('dodavanjeTurnira', DodavanjeTurniraView.as_view()),
    path('dojavaGreske', TacticErrorReportView.as_view()),
    path('removeLista', RemoveListView.as_view()),
    path('pregledTransakcija', PregledTransakcijaView.as_view()),
    path('zabrani', ZabraniPristupView.as_view()),
    path('placanjeClanarine', PlacanjeClanarineView.as_view()),
    path('deleteTaktika', ObrisiTaktikuView.as_view()),
    path('pregledTransakcija', PregledTransakcijaView.as_view()),
    path('rangLista', RangListaView.as_view()),
    path('listaDojavaPogreski', DojavaPogreskiView.as_view()),
    path('sviProfili', SviProfiliView.as_view()),
    path('detaljanProfil', DetaljanProfilView.as_view())
]
