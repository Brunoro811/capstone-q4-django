from uuid import uuid4

from django.db import models
from django.utils import timezone


class StoreModel(models.Model):

    class Meta:
        verbose_name= 'store'
        verbose_name_plural= 'stores'
        abstract= False
        db_table='stores'

    
    id = models.UUIDField(primary_key=True,default=uuid4,editable=False)
    name = models.CharField(max_length=255,unique=True)
    street = models.CharField(max_length=255)
    number = models.IntegerField()
    zip_code = models.CharField(max_length=9)
    state = models.CharField(max_length=100)
    other_information = models.CharField(max_length=150)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
