from django.urls import path
from .views import upgrade_me, ProfileView

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('upgrade/', upgrade_me, name='upgrade')
]
