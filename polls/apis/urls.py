from django.urls import path
from . import views

urlpatterns = [
    path('getpoll/', views.getPolls),
    path('addpoll/', views.postPolls),
    path('addoptions/',views.addOptions),
    path('getoptions/',views.getOptions),
    path("<int:poll_id>/results/", views.getResults),

]