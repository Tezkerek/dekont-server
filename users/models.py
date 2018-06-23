import string
import random

from django.db import models
import django.contrib.auth.models as auth_models

from groups.models import Group

# Create your models here.

class UserManager(auth_models.BaseUserManager):
    def _create_user(self, email, password, **extra_fields):
        """
        Creates a user with the given fields.
        """
        normalized_email = self.normalize_email(email)

        user = self.model(email=normalized_email, **extra_fields)
        user.set_password(password)

        user.save()
        return user

    def create_user(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        extra_fields.setdefault('is_group_admin', False)

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)

# Extended user
class User(auth_models.AbstractBaseUser, auth_models.PermissionsMixin):
    """
    Represents a user
    """

    email = models.EmailField(max_length=254, unique=True)
    username = models.CharField(max_length=64)

    # Relationship to group
    group = models.ForeignKey(Group, on_delete=models.SET_NULL, related_name='users', null=True)

    # Parent and children
    parent = models.ForeignKey('self', on_delete=models.SET_NULL, related_name='children', null=True)

    # Flags
    is_group_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    # Compatibility with Django's user system
    # Login with email
    USERNAME_FIELD = 'email'

    objects = UserManager()
