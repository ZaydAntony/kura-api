from django.urls import path
from . import views

urlpatterns = [
    path('polls_list/', views.list_polls , name="poll_list"),
    path('create_poll/', views.create_poll, name="create_poll"),
    path('<int:poll_id>/', views.poll_detail),
    path("<int:poll_id>/results/", views.getResults),

]