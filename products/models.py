from uuid import uuid4

from django.db import models


class ProductModel(models.Model):
    
    class Meta:
        verbose_name = 'product'
        verbose_name_plural= ' products'
        abstract = False
        db_table = 'products'
    
    id = models.UUIDField(primary_key=True,default=uuid4,editable=False)
    name = models.CharField(max_length=255)
    cost_value = models.FloatField()
    sale_value_retail = models.FloatField()
    sale_value_wholesale = models.FloatField()
    quantity_wholesale = models.IntegerField()
    
    store_id = models.ForeignKey("stores.StoreModel",on_delete=models.PROTECT, related_name='store',db_column='store_id')
    category_id = models.ForeignKey("categorys.CategoryModel",on_delete=models.PROTECT, related_name='category',db_column='category_id')

