from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from typing import Any


class UserManager(BaseUserManager):
    def create_user(self, email:str, password:str|None=None, **extra_fields:dict[str:Any]):
        """Creates and returns a regular user"""

        if not email:
            raise ValueError("User must have a Email address")

        for key,val in extra_fields.items():
            if key == 'email':
                extra_fields['email']= self.normalize_email(val)
            else:
                if key != 'is_active' or key != 'is_staff' or key != 'is_superuser':
                    extra_fields[key] = val.upper()

        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone, password:str|None=None, **extra_fields):
        """Creates and returns a superuser"""

        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(phone, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(null=True, blank=True,max_length=255)
    email = models.EmailField(unique=True)
        
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"