from rest_framework import serializers
from rest_framework.exceptions import PermissionDenied

from core.serializers import DekontModelSerializer

from .models import Group

class GroupSerializer(DekontModelSerializer):
    group_admin = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Group
        fields = ('id', 'name', 'invite_code', 'users', 'group_admin')
        read_only_fields = ('id', 'invite_code', 'users')
        admin_only_fields = {
            'create': (),
            'update': ('name',)
        }

    def get_group_admin(self, obj):
        return obj.group_admin.id

    def validate(self, data):
        request = self.context['request']
        action = self.context['action']
        user = request.user

        # Check if non-admin is trying to set admin-only fields
        if not user.is_group_admin and set(data.keys()) & set(self.Meta.admin_only_fields[action]):
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
