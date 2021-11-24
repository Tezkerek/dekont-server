from django.utils.translation import ugettext_lazy as _
from django.contrib.auth import get_user_model, authenticate

from rest_framework import serializers

from .models import Token
from .utils import get_username_field


User = get_user_model()
USERNAME_FIELD = get_username_field()

class ObtainTokenSerializer(serializers.Serializer):
    class Meta:
        model = Token

    password = serializers.CharField(
        label=_("Password"),
        style={'input_type': 'password'},
        trim_whitespace=False
    )
    name = serializers.CharField(
        max_length=Meta.model._meta.get_field('name').max_length,
        label=_("Token Name")
    )

    def __init__(self, *args, **kwargs):
        super(ObtainTokenSerializer, self).__init__(*args, **kwargs)

        # Dynamically add the USERNAME_FIELD
        self.fields[USERNAME_FIELD] = serializers.CharField(
            max_length=User._meta.get_field(USERNAME_FIELD).max_length,
            label=_(USERNAME_FIELD.capitalize())
        )

    def validate(self, attrs):
        username = attrs.get(USERNAME_FIELD)
        password = attrs.get('password')

        if username and password:
            user = authenticate(request=self.context.get('request'),
                                username=username, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "{}" and "password".'.format(USERNAME_FIELD))
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs
