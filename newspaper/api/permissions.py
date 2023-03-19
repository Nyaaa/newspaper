from rest_framework import permissions
from news.models import Author


class UserPermission(permissions.BasePermission):

    def has_permission(self, request, view):
        if view.action in ['list', 'retrieve']:
            return True
        elif view.action in ['create', 'update', 'partial_update', 'destroy']:
            return request.user.is_authenticated and Author.objects.filter(user=request.user).exists()
        else:
            return False
