from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class MultiAuthTokenConfig(AppConfig):
    name = 'rest_framework_multiauthtoken'
    verbose_name = _("Multiple Tokens Auth")
