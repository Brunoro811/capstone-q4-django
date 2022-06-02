from functools import reduce
from typing import List

from accounts.models import AccountModel
from django.db.models import Model
from products.models import ProductModel
from rest_framework.authentication import TokenAuthentication
from rest_framework.exceptions import NotFound
from rest_framework.generics import ListCreateAPIView
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework.serializers import ValidationError
from variations.models import VariationModel

from orders.exceptions import (
    ProductNotAssociatedOwnStoreError,
    UnavaliableStockQuantityError,
    VariationNotFoundError,
)
from orders.models import OrdersModel, OrderVariationsModel
from orders.permissions import (
    ListCreateOrderAuthenticatePermission,
    ListCreateOrderAuthorizePermission,
)
from orders.serializers import CreateOrderSerializer


class ListCreateOrderView(ListCreateAPIView):
    authentication_classes = [TokenAuthentication]
    permission_classes = [
        ListCreateOrderAuthenticatePermission,
        ListCreateOrderAuthorizePermission,
    ]
    serializer_class = CreateOrderSerializer
    queryset = OrdersModel.objects.all()

    def get_or_fail(self, payload):
        variation: VariationModel = VariationModel.objects.filter(
            pk=payload["id"]
        ).first()

        if not variation:
            raise VariationNotFoundError(payload["id"])

        seller: AccountModel = self.request.user
        if seller.store_id.id != variation.product_id.store_id.id:
            raise ProductNotAssociatedOwnStoreError(variation.product_id)

        if payload["quantity"] > variation.quantity:
            raise UnavaliableStockQuantityError(payload["quantity"], variation)

        return variation

    def get_sale_value(self, info):
        product: ProductModel = info["variation"].product_id
        return (
            product.sale_value_wholesale
            if (info["quantity"] >= product.quantity_wholesale)
            else product.sale_value_retail
        )

    def ajust_stock(self, order: OrdersModel):
        ord_var_list: List[OrderVariationsModel] = OrderVariationsModel.objects.filter(
            order_id=order.id
        )

        info = [(ord_var.variation, ord_var.quantity) for ord_var in ord_var_list]

        for var, quantity in info:
            var.quantity -= quantity

        var_list = [var for var, _ in info]

        VariationModel.objects.bulk_update(var_list, ["quantity"])

    def post(self, request: Request, *args, **kwargs):
        input: CreateOrderSerializer = self.get_serializer(data=request.data)
        input.is_valid(raise_exception=True)

        variations_info = input.data.pop("variations")
        seller: AccountModel = request.user

        if not seller.store_id:
            raise ...

        variations = [
            {
                "variation": self.get_or_fail(info),
                "quantity": info["quantity"],
            }
            for info in variations_info
        ]

        order: OrdersModel = OrdersModel.objects.create(
            seller=seller, store=seller.store_id, total_value=0
        )

        ord_vars = [
            OrderVariationsModel(
                **{
                    **info,
                    "sale_value": self.get_sale_value(info),
                    "order": order,
                }
            )
            for info in variations
        ]

        orders_vars = OrderVariationsModel.objects.bulk_create(ord_vars)

        sum = reduce(
            lambda acc, ord_var: acc + (ord_var.sale_value * ord_var.quantity),
            orders_vars,
            0,
        )

        order.total_value = sum

        order.save()

        self.ajust_stock(order)

        output = ...

        return Response({"info": "deu bom"})
