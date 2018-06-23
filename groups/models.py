import string
import random

from django.db import models

class Group(models.Model):
    """
    Represents a group of users
    """
    def __str__(self):
        return self.name

    name = models.CharField(max_length=100)
    invite_code = models.CharField(max_length=8, unique=True)

    @property
    def group_admin(self):
        """
        The user who is group admin, or None if admin is not set
        """
        result_queryset = self.users.filter(is_group_admin=True)
        return result_queryset[0] if len(result_queryset) > 0 else None

    @group_admin.setter
    def group_admin(self, user):
        """
        Sets the new group admin
        """
        # Unset previous admin, if set
        prev_admin = self.group_admin
        if prev_admin is not None:
            prev_admin.is_group_admin = False
            prev_admin.save()

        user.group = self
        user.is_group_admin = True
        user.save()

    def save(self, *args, **kwargs):
        if not self.invite_code:
            self.invite_code = self.generate_invite_code()

        return super().save(*args, **kwargs)

    @classmethod
    def generate_invite_code(cls, length=6):
        return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))
