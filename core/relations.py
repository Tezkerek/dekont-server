from django.core.exceptions import ObjectDoesNotExist
from django.utils.translation import ugettext_lazy as _
from rest_framework.relations import HyperlinkedRelatedField

class PkHyperlinkedRelatedField(HyperlinkedRelatedField):
    default_error_messages = {
        'required': _('This field is required.'),
        'does_not_exist': _('Invalid pk "{pk_value}" - object does not exist.'),
        'incorrect_type': _('Incorrect type. Expected pk value, received {data_type}.'),
    }

    pk_field_name = 'id'

    def __init__(self, *args, **kwargs):
        self.pk_field_name = kwargs.pop('pk_field_name', self.pk_field_name)

        return super().__init__(*args, **kwargs)

    def to_internal_value(self, data):
        """
        Takes only PKs.
        """
        # Taken from PrimaryKeyRelatedField
        try:
            return self.get_queryset().get(pk=data)
        except ObjectDoesNotExist:
            self.fail('does_not_exist', pk_value=data)
        except (TypeError, ValueError):
            self.fail('incorrect_type', data_type=type(data).__name__)

    def to_representation(self, value):
        return {
            self.pk_field_name: value.pk,
            'url': super().to_representation(value),
        }
