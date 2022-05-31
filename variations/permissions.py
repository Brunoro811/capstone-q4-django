from rest_framework.permissions import BasePermission, IsAuthenticated
from rest_framework.request import Request
from stokar.permissions import (
    GenericAuthenticatedPermission,
    GenericAuthorizedPermission,
)


class ListCreateAuthenticatePermission(GenericAuthenticatedPermission):
    AUTHENTICATED_METHODS = (
        "GET",
        "POST",
    )

    def __init__(self):
        super().__init__(methods=self.AUTHENTICATED_METHODS)


class ListCreateAuthorizePermission(GenericAuthorizedPermission):
    AUTHORIZED_METHODS = ("POST",)

    def __init__(self):
        super().__init__(methods=self.AUTHORIZED_METHODS, allow_admin=True)
