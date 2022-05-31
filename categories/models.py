from uuid import uuid4

from django.db import models


class CategoryModel(models.Model):
    
    id = models.UUIDField(primary_key=True,editable=False,default=uuid4)
    name = models.CharField(max_length=255)
