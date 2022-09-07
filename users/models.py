import uuid
from django.contrib.auth.models import AbstractUser
from django.db import models
from users.utils import CustomUserManager

class User(AbstractUser):
    id=models.UUIDField(primary_key=True,default=uuid.uuid4,unique=True,editable=False,max_length=36)
    username = models.CharField(max_length=128, unique=True)
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=50)
    is_seller = models.BooleanField()

    REQUIRED_FIELDS = ["first_name", "last_name", "is_seller"]

    objects = CustomUserManager()