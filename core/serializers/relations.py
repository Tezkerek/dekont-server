from django.core.exceptions import ObjectDoesNotExist
from django.db.models import QuerySet, Manager
from django.utils.translation import ugettext_lazy as _
from rest_framework.relations import HyperlinkedRelatedField

class DynamicQuerySetMixin:
    """
    Serializer mixin with a special `get_queryset()` method that lets you pass
    a callable for the queryset kwarg. This enables you to limit the queryset
    based on data or context available on the serializer at runtime.
    Taken from https://stackoverflow.com/a/33490429/4904553
    """

    def get_queryset(self):
        """
        Return the queryset for a related field. If the queryset is a callable,
        it will be called with one argument which is the field instance and
        should return a queryset or model manager.
        .. code::
            def get_my_limited_queryset(field):
                root = field.root
                if root.instance is None:
                    return MyModel.objects.none()
                return root.instance.related_set.all()
            MySerializer(queryset=get_my_limited_queryset)
        """
        queryset = self.queryset
        if callable(queryset):
            queryset = queryset(self)
        if isinstance(queryset, (QuerySet, Manager)):
            # Ensure queryset is re-evaluated whenever used.
            # Note that actually a `Manager` class may also be used as the
            # queryset argument. This occurs on ModelSerializer fields,
            # as it allows us to generate a more expressive 'repr' output
            # for the field.
            # Eg: 'MyRelationship(queryset=ExampleModel.objects.all())'
            queryset = queryset.all()

        return queryset

class PkHyperlinkedRelatedField(DynamicQuerySetMixin, HyperlinkedRelatedField):
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
