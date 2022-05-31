from uuid import uuid4

from django.db import models


class VariationModel(models.Model):
    class Meta:
        verbose_name= 'variation'
        verbose_name_plural= 'variations'
        abstract= False
        db_table='variations'
    
    id = models.UUIDField(primary_key=True,default=uuid4,editable=False)
    size = models.CharField(max_length=50)
    quantity = models.IntegerField()
    color = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)

    product_id = models.ForeignKey("products.ProductModel",on_delete=models.PROTECT,db_column='product_id',related_name='variations')
