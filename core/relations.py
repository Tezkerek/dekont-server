from rest_framework.relations import HyperlinkedRelatedField

class PkHyperlinkedRelatedField(HyperlinkedRelatedField):
    pk_field_name = 'id'

    def __init__(self, *args, **kwargs):
        self.pk_field_name = kwargs.pop('pk_field_name', self.pk_field_name)

        return super().__init__(*args, **kwargs)

    def to_representation(self, value):
        return {
            self.pk_field_name: value.pk,
            'url': super().to_representation(value),
        }
