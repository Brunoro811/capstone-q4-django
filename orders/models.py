from uuid import uuid4

from django.db import models


class OrdersModel(models.Model):
    class Meta:
        verbose_name= 'order'
        verbose_name_plural= 'orders'
        abstract= False
        db_table='orders'
    
    id = models.UUIDField(primary_key=True,default=uuid4,editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    total_value = models.FloatField()

    seller = models.ForeignKey("accounts.AccountModel", on_delete=models.PROTECT,related_name="+")
    store = models.ForeignKey("stores.StoreModel", on_delete=models.PROTECT,related_name="+")
    
    variations = models.ManyToManyField("variations.VariationModel", related_name='+', through='orders.OrderVariationsModel')


class OrderVariationsModel(models.Model):
    class Meta:
        verbose_name= 'order_variation'
        verbose_name_plural= 'orders_variations'
        abstract= False
        db_table='orders_variations'
    
    id = models.UUIDField(primary_key=True,default=uuid4,editable=False)
    
    order = models.ForeignKey("orders.OrdersModel", on_delete=models.PROTECT)
    variation = models.ForeignKey("variations.VariationModel",on_delete=models.PROTECT)
    
    sale_value = models.FloatField()
    quantity = models.IntegerField()

    

    