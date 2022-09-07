import uuid
from django.contrib.auth.models import BaseUserManager


class CustomUserManager(BaseUserManager):
    def create_superuser(self,username, password, **extra_fields):
        if not username:
            raise ValueError('username is required')

        username = self.normalize_email(username)

        user = self.model(username=username, is_superuser=True, is_seller=False, **extra_fields)

        user.set_password(password)

        user.save(using=self.db)

        return user

    def create_user(self,username, password, is_seller, **extra_fields):
        if not username:
            raise ValueError('username is required')

        username = self.normalize_email(username)

        user = self.model( username=username, is_superuser=False, is_seller=is_seller, **extra_fields)

        user.set_password(password)

        user.save(using=self.db)

        return user