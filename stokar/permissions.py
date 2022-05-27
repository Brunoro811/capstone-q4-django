from rest_framework.permissions import BasePermission
from rest_framework.request import Request


class GenericAuthenticatedPermission(BasePermission):

    """
    Generic class that constructs authenticated routes' validation.
    """

    AUTHENTICATED_METHODS = ...

    def __init__(self, **kwargs):
        """
        Initializes authentication class.\n
        Keyword args:\n
        `methods` - TUPLE - receives uppercased authenticated methods.
        """
        self.AUTHENTICATED_METHODS = kwargs.get("methods", ())

    def has_permission(self, request: Request, view):

        if request.method in self.AUTHENTICATED_METHODS:
            return bool(request.user.is_authenticated)

        return True


class GenericAuthorizedPermission(BasePermission):

    """
    Generic class thar constructs permission validation.
    """

    AUTHORIZED_METHODS = ...
    ALLOW_ADMIN = ...
    ALLOW_SELLER = ...

    def __init__(self, **kwargs):
        """
        Initializes permission class.\n
        Keyword args:\n
        `methods` - TUPLE - receives uppercased authenticated methods\n
        `allow_admin` - BOOL - if True, indicates informed methods are permited
            to admin user.\n
        `allow_seller` - BOOL - if True, indicates informed methods are permited
            to seller user.
        """
        self.AUTHORIZED_METHODS = kwargs.get("methods", ())
        self.ALLOW_ADMIN = kwargs.get("allow_admin", False)
        self.ALLOW_SELLER = kwargs.get("allow_seller", False)

    def has_permission(self, request: Request, view):
        return self.check_permission(request)

    def is_admin(self, request: Request) -> bool:
        """
        Checks if user is admin
        """
        return request.user.is_admin

    def is_seller(self, request: Request) -> bool:
        """
        Checks if user is seller
        """
        return request.user.is_seller

    def check_if_user_has_permission(self, request: Request) -> bool:
        """
        Checks user's type and returns if this route is allowed to it.
        """

        if self.is_admin(request):
            return self.ALLOW_ADMIN

        if self.is_seller(request):
            return self.ALLOW_SELLER

        raise TypeError("User's seller and admin info does not match with type rules")

    def check_permission(self, request: Request) -> bool:
        """
        Checks identity for AUTHORIZED_METHODS
        """

        if request.method in self.AUTHORIZED_METHODS:
            return self.check_if_user_has_permission(request)

        return True
