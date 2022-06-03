from products.models import ProductModel
from rest_framework.exceptions import APIException, NotFound
from rest_framework.status import (
    HTTP_400_BAD_REQUEST,
    HTTP_403_FORBIDDEN,
    HTTP_404_NOT_FOUND,
    HTTP_422_UNPROCESSABLE_ENTITY,
)
from variations.models import VariationModel


class BadRequestError(APIException):
    status_code = HTTP_400_BAD_REQUEST
    default_code = "bad request"


class ForbiddenError(APIException):
    status_code = HTTP_403_FORBIDDEN
    default_code = "forbidden"


class NotFoundError(APIException):
    status_code = HTTP_404_NOT_FOUND
    default_code = "not found"


class UnprocessableEntityError(APIException):
    status_code = HTTP_422_UNPROCESSABLE_ENTITY
    default_code = "unprocessable entity"


class ProductNotAssociatedOwnStoreError(ForbiddenError):
    detail = ...

    def __init__(self, product: ProductModel):
        self.detail = {
            "detail": "Product not associated to seller's related store.",
            "products": [
                {
                    "id": product.id,
                    "name": product.name,
                },
            ],
        }


class UnavaliableStockQuantityError(UnprocessableEntityError):
    detail = ...

    def __init__(self, demanded: int, variation: VariationModel):
        self.detail = {
            "detail": "Insuficient quantity on stock.",
            "variations": [
                {
                    "id": variation.id,
                    "ordered_quantity": demanded,
                    "available_quantity": variation.quantity,
                }
            ],
        }


class VariationNotFoundError(NotFoundError):
    detail = ...

    def __init__(self, id):
        self.detail = {"detail": "variation not found", "variation": {"id": id}}


class SellerNotAssociatedToAnyStoreError(ForbiddenError):
    default_detail = {"detail": "Seller not associated to any store yet."}


class NotSellerError(ForbiddenError):
    default_detail = {"detail": "You do not have permission to perform this action."}


class EmpyVariationsError(BadRequestError):
    default_detail = {"detail": "You must provide at least one variation."}
