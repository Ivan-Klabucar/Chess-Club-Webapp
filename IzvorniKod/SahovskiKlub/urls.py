from django.urls import path
from django.contrib.auth import views
from .views import HomeView, RegisterView

urlpatterns = [
    path('', HomeView.as_view()),
    path('logout', views.LogoutView.as_view()),
    path('login', views.LoginView.as_view()),
    path('register', RegisterView.as_view()),
]