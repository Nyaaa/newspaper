from django.urls import path
from .views import upgrade_me, ProfileView, NameEditView

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('upgrade/', upgrade_me, name='upgrade'),
    path('name_edit/', NameEditView.as_view(), name='name_edit'),
]
