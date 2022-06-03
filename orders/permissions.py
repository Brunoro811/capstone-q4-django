from stokar.permissions import (
    GenericAuthenticatedPermission,
    GenericAuthorizedPermission,
)


class ListCreateOrderAuthenticatePermission(GenericAuthenticatedPermission):
    AUTHENTICATED_METHODS = (
        "GET",
        "POST",
    )

    def __init__(self):
        super().__init__(methods=self.AUTHENTICATED_METHODS)


class ListCreateOrderAuthorizePermission(GenericAuthorizedPermission):
    AUTHORIZED_METHODS = (
        "POST",
        "GET",
    )

    def __init__(self):
        super().__init__(
            methods=self.AUTHORIZED_METHODS, allow_admin=True, allow_seller=True
        )
