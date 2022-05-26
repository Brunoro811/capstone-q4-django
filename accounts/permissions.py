from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.request import Request


class IsAuthenticatedAccounts(IsAuthenticated):
    
    def has_permission(self, request, view):
        restrict_methods = ('GET','PATCH',)
        if request.method in restrict_methods:
            return super().has_permission(request, view)
        return True
