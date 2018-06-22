from rest_framework.authentication import TokenAuthentication

from .models import Token

# Extend DRF's token auth class to use our custom Token model
class MultiAuthTokenAuthentication(TokenAuthentication):
    model = Token
