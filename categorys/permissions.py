from stokar.permissions import (
    GenericAuthenticatedPermission,
    GenericAuthorizedPermission,
)


class CreateAuthenticatePermission(GenericAuthenticatedPermission):
    AUTHENTICATED_METHODS = ("POST",)

    def __init__(self):
        super().__init__(methods=self.AUTHENTICATED_METHODS)


class CreateAuthorizePermission(GenericAuthorizedPermission):
    AUTHORIZED_METHODS = ("POST",)

    def __init__(self):
        super().__init__(methods=self.AUTHORIZED_METHODS, allow_admin=True)
