from django.urls import path
from django.contrib.auth import views
from .views import HomeView, DemoTacticView, sign_up, listaTaktika, obavijesti

urlpatterns = [
    path('', HomeView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('login', views.LoginView.as_view()),
    path('register', sign_up, name="sign-up"),
    path('dnevneTaktike', listaTaktika, name="listaTaktkika"),
    path('taktika', DemoTacticView.as_view()),
    path('obavijesti', obavijesti, name="obavijesti")
]
