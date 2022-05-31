from uuid import uuid4

from django.db import models


class CategoryModel(models.Model):
    class Meta:
        verbose_name= 'category'
        verbose_name_plural= 'categories'
        abstract= False
        db_table='categories'
    
    
    id = models.UUIDField(primary_key=True,editable=False,default=uuid4)
    name = models.CharField(max_length=255)
