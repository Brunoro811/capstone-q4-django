from products.models import ProductModel
from rest_framework.exceptions import APIException, NotFound
from rest_framework.status import (
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_409_CONFLICT,
    HTTP_422_UNPROCESSABLE_ENTITY,
)
from variations.models import VariationModel


class ForbiddenError(APIException):
    status_code = HTTP_403_FORBIDDEN
    default_code = "forbidden"


class UnprocessableEntityError(APIException):
    status_code = HTTP_422_UNPROCESSABLE_ENTITY
    default_code = "unprocessable entity"


class VariationNotFoundError(NotFound):
    default_detail = {"name": ["category with this name already exists."]}

    def __init__(self, detail=None, code=None):
        ...


class ProductNotAssociatedOwnStoreError(ForbiddenError):
    detail = ...

    def __init__(self, product: ProductModel):
        self.detail = {
            "detail": "Product not associated to seller's related store.",
            "product": {
                "id": product.id,
                "name": product.name,
            },
        }
