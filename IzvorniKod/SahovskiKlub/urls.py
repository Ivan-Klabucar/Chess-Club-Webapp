from django.urls import path
from django.contrib.auth import views
from .views import HomeView, RegisterView, DemoTacticView, listaTaktika, novosti


urlpatterns = [
    path('', HomeView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('login', views.LoginView.as_view()),
    path('register', RegisterView.as_view()),
    path('dnevneTaktike', listaTaktika, name="listaTaktkika"),
    path('taktika', DemoTacticView.as_view()),
    path('novosti', novosti, name="novosti")
]
