from rest_framework import status
from rest_framework.exceptions import APIException


class StoreNameAlreadyExists(APIException):
    status_code = status.HTTP_409_CONFLICT
    default_detail = {"name": ["store with this name already exists."]}
