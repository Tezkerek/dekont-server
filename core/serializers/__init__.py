from rest_framework import serializers

from .fields import AmountField, PkAndUrlReverseField
from .relations import PkHyperlinkedRelatedField

class PerActionFieldsMixin(object):
    """
    Dynamically sets ModelSerializer fields depending on action, as declared in the serializer class.
    """

    def __init__(self, *args, **kwargs):
        self.set_per_action_fields()

        super().__init__(*args, **kwargs)

    def set_per_action_fields(self):
        """
        Sets the serializer's Meta's fields, read_only_fields, extra_kwargs to the ones defined in 
        Meta.per_action_fields, which is a dict that looks like this:

            per_action_fields = {
                'action': {
                    # Just like Meta's properties, fields is required, the other two are optional
                    'fields': ('id', 'username', 'email', 'password'),
                    'read_only_fields': ('username',),
                    'extra_kwargs': {'password': {'write_only': True}}
                }
            }
        """
        if hasattr(self.Meta, 'per_action_fields'):
            per_action_fields = self.Meta.per_action_fields

            assert isinstance(per_action_fields, dict), '{} should be a dict'.format('Meta.per_action_fields')

            action = self.get_action()

            # Set the fields property on the serializer's Meta class, if defined for the action
            if action in per_action_fields.keys():
                fields = per_action_fields[action]

                assert 'fields' in fields, \
                    '{}[{}] should contain a list of fields'.format('Meta.per_action_fields', action)

                self.Meta.fields = fields['fields']

                # Extra field attributes
                if 'read_only_fields' in fields:
                    self.Meta.read_only_fields = fields['read_only_fields']
                if 'extra_kwargs' in fields:
                    self.Meta.extra_kwargs = fields['extra_kwargs']

    def get_action(self):
        assert 'action' in self.context, (
            "You should pass {} to the serializer's context, or override {} to return the action."
            .format('action', 'get_action')
        )

        return self.context['action'].split('-').pop()

class DekontModelSerializer(serializers.ModelSerializer):
    """
    A ModelSerializer to be used for serializing Dekont models.
    """
    pass

class PkHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    serializer_related_field = PkHyperlinkedRelatedField
