from uuid import uuid4

from django.db import models


class StoreModel(models.Model):
    
    id = models.UUIDField(primary_key=True,default=uuid4,editable=False)
    name = models.CharField(max_length=255,unique=True)
    street = models.CharField(max_length=255)
    number = models.IntegerField()
    zip_code = models.CharField(max_length=9)
    state = models.CharField(max_length=10)
    other_information = models.CharField(max_length=150)
