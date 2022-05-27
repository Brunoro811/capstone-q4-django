from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class AccountModel(AbstractUser):
    
    id = models.UUIDField(primary_key=True,default=uuid4,editable=False)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=150,null=False)
    last_name = models.CharField(max_length=255)
    is_seller = models.BooleanField()
    is_admin = models.BooleanField()
    created_at = models.DateTimeField(default=timezone.now,editable=False)

    store = models.ForeignKey("stores.StoreModel",on_delete=models.PROTECT,db_column='store_id',related_name='sellers', null=True)
