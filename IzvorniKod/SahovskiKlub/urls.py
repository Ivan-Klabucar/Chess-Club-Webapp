from django.urls import path
from django.contrib.auth import views
from global_login_required import login_not_required
from .views import HomeView, sign_up

urlpatterns = [
    path('', HomeView.as_view()),
    path('login', login_not_required(views.LoginView.as_view())),
    path('register', sign_up, name="sign-up"),
]