from django.urls import path
from . import views

urlpatterns =[
    path('cast-vote/', views.cast_vote),
]