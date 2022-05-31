from rest_framework.permissions import BasePermission
from rest_framework.request import Request
from stokar.permissions import (
    GenericAuthenticatedPermission,
    GenericAuthorizedPermission,
)


class IsAdmin(BasePermission):
    def has_permission(self, request: Request, _):
        return not (request.user.is_anonymous or not request.user.is_admin)


class CreateAuthenticatePermission(GenericAuthenticatedPermission):
    AUTHENTICATED_METHODS = ("POST",)

    def __init__(self):
        super().__init__(methods=self.AUTHENTICATED_METHODS)


class CreateAuthorizePermission(GenericAuthorizedPermission):
    AUTHORIZED_METHODS = ("POST",)

    def __init__(self):
        super().__init__(methods=self.AUTHORIZED_METHODS, allow_admin=True)
