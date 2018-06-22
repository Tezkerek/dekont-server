from django.db import models
from django.conf import settings
from django.utils.translation import ugettext_lazy as _
from django.utils.encoding import python_2_unicode_compatible

from rest_framework.authtoken.models import Token as SingleToken


@python_2_unicode_compatible
class Token(SingleToken):
    # key is no longer pk
    key = models.CharField(_("Key"), max_length=40, db_index=True, unique=True)

    # user relation is now a foreign key, not a one-to-one relation
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='auth_tokens',
        on_delete=models.CASCADE,
        verbose_name=_("User")
    )

    # Identifier for the token
    name = models.CharField(_("Name"), max_length=64)

    class Meta:
        unique_together = (('user', 'name'),)
