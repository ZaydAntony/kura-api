from django.urls import path
from . import views

urlpatterns = [
    path('getpoll/', views.getPolls),
    path('addpoll/', views.postPolls),
]