from django.urls import path
from .views import login, logout, change_password, refresh_token

urlpatterns = [
    path('auth/login/', login, name='login'),
    path('auth/logout/', logout, name='logout'),
    path('auth/change-password/', change_password, name='change_password'),
    path('auth/refresh/', refresh_token, name='refresh_token'),
]
