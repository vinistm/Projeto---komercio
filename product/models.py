import uuid
from django.db import models


class Product(models.Model):
    id = models.UUIDField(default=uuid.uuid4, primary_key=True,editable=False)
    description = models.CharField(max_length=280)
    price = models.FloatField()
    quantity = models.IntegerField()
    is_active = models.BooleanField(default=True)

    seller = models.ForeignKey('users.User', on_delete=models.CASCADE, related_name='product')