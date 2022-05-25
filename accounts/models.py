from uuid import uuid4

from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class AccountModel(AbstractUser):
    
    id = models.UUIDField(primary_key=True,default=uuid4,editable=False)
    email = models.EmailField(unique=True)
    last_name = models.CharField(max_length=255)
    is_seller = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    created_at = models.DateTimeField(default=timezone.now,editable=False)

    store = models.ForeignKey("stores.StoreModel",on_delete=models.CASCADE,db_column='store_id')
