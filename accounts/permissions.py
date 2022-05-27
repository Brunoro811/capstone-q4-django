from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.request import Request


class IsAuthenticatedAccounts(IsAuthenticated):
    
    def has_permission(self, request, view):
        restrict_methods = ('GET','POST','PATCH',)
        if request.method in restrict_methods:
            return super().has_permission(request, view)
        return True


class IsAdmin(BasePermission):
    
    def has_permission(self, request, _):
        restrict_methods = ('POST',)
        if request.method in restrict_methods and (
            not request.user.is_admin
        ):
            return False

        return True
