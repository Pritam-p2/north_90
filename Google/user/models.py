from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from typing import Any

class CustomUserManager(BaseUserManager):
    def get_by_natural_key(self, username):
        return self.get(email=username)


class User(AbstractBaseUser, PermissionsMixin):
    name = models.CharField(null=True, blank=True,max_length=255)
    email = models.EmailField(unique=True)

    access = models.CharField(max_length=1000, blank=True, null=True)
    refresh = models.CharField(max_length=1000, blank=True, null=True)
    
    USERNAME_FIELD = "email"

    objects = CustomUserManager() 

    def __str__(self):
        return self.email