from rest_framework import status
from rest_framework.exceptions import APIException


class ConflictError(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_code = "conflict"


class AlreadyRegisteredEmailError(ConflictError):
    default_detail = {"email": ["user with this email already exists."]}


class AlreadyRegisteredUsernameError(ConflictError):
    default_detail = {"username": ["user with this username already exists."]}
