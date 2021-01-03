from django.urls import path
from django.contrib.auth import views
from .views import HomeView, RegisterView
from .views import TreninziView, DodavanjeTreningaView, TurniriView, DodavanjeTurniraView
from .views import NovostiView, ObjavaNovostiView
from .views import ListaTaktikaView
from .views import ProfileView
from .views import RemoveListView
from .views import PregledTransakcijaView
from .views import DemoTacticView, TacticCreationView, TacticRevisionView, TacticErrorReportView
from .views import PlacanjeClanarineView

urlpatterns = [
    path('', HomeView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('login', views.LoginView.as_view()),
    path('register', RegisterView.as_view()),
    path('dnevneTaktike', ListaTaktikaView.as_view()),
    path('taktika', DemoTacticView.as_view()),
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
    path('placanjeClanarine', PlacanjeClanarineView.as_view())
]
