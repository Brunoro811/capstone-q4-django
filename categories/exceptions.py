from rest_framework.exceptions import APIException
from rest_framework.status import HTTP_409_CONFLICT


class ConflictError(APIException):
    status_code = HTTP_409_CONFLICT
    default_code = "conflict"


class AlreadyRegisteredNameError(ConflictError):
    default_detail = {"name": ["category with this name already exists."]}
