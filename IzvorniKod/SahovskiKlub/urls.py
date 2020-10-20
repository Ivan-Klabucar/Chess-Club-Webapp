from django.urls import path
from django.contrib.admin import views
from .views import HomeView

urlpatterns = [
    path('', HomeView.as_view())
]