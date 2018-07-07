from rest_framework import serializers

from .relations import PkHyperlinkedRelatedField

class PkHyperlinkedModelSerializer(serializers.HyperlinkedModelSerializer):
    serializer_related_field = PkHyperlinkedRelatedField
