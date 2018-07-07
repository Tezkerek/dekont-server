from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from core.fields import PkAndUrlReverseField
from core.relations import PkHyperlinkedRelatedField
from core.serializers import PkHyperlinkedModelSerializer

from .models import Group

class GroupSerializer(PkHyperlinkedModelSerializer):
    group_admin = PkAndUrlReverseField(view_name='user-detail', read_only=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'invite_code', 'users', 'group_admin')
        read_only_fields = ('id', 'invite_code', 'users')
        admin_only_fields = ('name',)

    def validate(self, data):
        user = self.context['request'].user

        # Check if non-admin is trying to set admin-only fields
        if not user.is_group_admin and set(data.keys()) & set(self.Meta.admin_only_fields):
            raise PermissionDenied('Only a group admin may set these fields: ' + ', '.join(self.Meta.admin_only_fields))

        return data

    def create(self, validated_data):
        group_admin = validated_data.pop('group_admin', None)

        group = self.Meta.model(**validated_data)

        group.save()

        if group_admin is not None:
            group.group_admin = group_admin

        return group

class GroupJoinSerializer(serializers.Serializer):
    invite_code = serializers.CharField(max_length=Group._meta.get_field('invite_code').max_length)
