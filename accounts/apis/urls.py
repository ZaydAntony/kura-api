from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from . import views
from django.urls import path
urlpatterns = [

    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'), #User login
    path('refresh/', TokenRefreshView.as_view(), name='token_refresh'),# refresh
    path('register/', views.register_user, name='register_user'), # user signup
]