from rest_framework import serializers
from rest_framework.reverse import reverse

from core.fields import PkAndUrlReverseField

from .models import Group

class GroupSerializer(serializers.HyperlinkedModelSerializer):
    group_admin = PkAndUrlReverseField(view_name='user-detail')

    class Meta:
        model = Group
        fields = ('id', 'name', 'invite_code', 'group_admin')
        read_only_fields = ('id', 'invite_code', 'group_admin')

    def create(self, validated_data):
        group_admin = validated_data.pop('group_admin', None)

        group = self.Meta.model(**validated_data)

        group.save()

        if group_admin is not None:
            group.group_admin = group_admin

        return group

class GroupJoinSerializer(serializers.Serializer):
    invite_code = serializers.CharField(max_length=Group._meta.get_field('invite_code').max_length)
