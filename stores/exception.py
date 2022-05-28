from rest_framework import status
from rest_framework.exceptions import APIException


class StoreNameAlreadyExists(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = {"name": ["store with this name already exists."]}


class StoreIsAlreadyActive(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = {"detail": "store with this id is already active"}


class StoreIsAlreadyDeactivated(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = {"detail": "store with this id is already deactivated"}
