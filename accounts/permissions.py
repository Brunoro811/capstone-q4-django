from stokar.permissions import (
    GenericAuthenticatedPermission,
    GenericAuthorizedPermission,
)


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
