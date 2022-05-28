from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.request import Request
from stokar.permissions import (GenericAuthenticatedPermission,
                                GenericAuthorizedPermission)


class IsAuthenticatedAccounts(IsAuthenticated):
    
    def has_permission(self, request, view):
        restrict_methods = ('GET','POST','PATCH',)
        if request.method in restrict_methods:
            return super().has_permission(request, view)
        return True


class IsAdmin(BasePermission):
    
    def has_permission(self, request, _):
        restrict_methods = ('POST','GET',)
        if request.method in restrict_methods and (
            not request.user.is_admin
        ):
            return False

        return True

class RetrieveUpdateOneAuthenticatePermission(GenericAuthenticatedPermission):
    AUTHENTICATED_METHODS = (
        "GET",
        "PATCH",
    )

    def __init__(self):
        super().__init__(methods=self.AUTHENTICATED_METHODS)


class RetrieveUpdateOneAuthorizePermission(GenericAuthorizedPermission):
    AUTHORIZED_METHODS = (
        "GET",
        "PATCH",
    )

    def __init__(self):
        super().__init__(methods=self.AUTHORIZED_METHODS, allow_admin=True)

