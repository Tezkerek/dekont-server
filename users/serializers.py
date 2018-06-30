from rest_framework import serializers
from rest_framework.compat import authenticate
from rest_framework.reverse import reverse
from django.utils.translation import ugettext_lazy as _

from core.fields import PkAndUrlReverseField
from core.relations import PkHyperlinkedRelatedField

from .models import User


class UserRegistrationSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'password', 'is_group_admin')

    def create(self, validated_data):
        email = validated_data.pop('email')
        password = validated_data.pop('password')

        user = self.Meta.model.objects.create_user(email, password, **validated_data)
        return user

class UserSerializer(serializers.HyperlinkedModelSerializer):
    serializer_related_field = PkHyperlinkedRelatedField

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'username', 'group', 'approvers', 'reporters', 'is_group_admin')
        extra_kwargs = {
            'password': {'write_only': True},
            'approvers': {
                'read_only': False,
                'queryset': lambda field: field.root.instance.get_group_members()
            }
        }

    def to_internal_value(self, data):
        user = self.context['request'].user
        errors = {}

        internal_value = super().to_internal_value(data)

        # Per-field permissions
        if 'approvers' in data:
            if not user.is_group_admin:
                errors['approvers'] = "Only a group admin can modify this."
        if 'is_group_admin' in data:
            if not user.is_group_admin:
                errors['is_group_admin'] = "Only a group admin can modify this."
            elif user == self.instance and user.is_group_admin and not internal_value['is_group_admin']:
                errors['is_group_admin'] = \
                    "You cannot unset yourself as admin. Instead, make somebody else in your group admin"

        if errors:
            raise serializers.ValidationError(errors)

        return internal_value


    def update(self, instance, validated_data):
        # Fields not set with setattr()
        password = validated_data.pop('password', None)
        approvers = validated_data.pop('approvers', [])

        # Update attributes
        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        # Set password properly
        if password is not None:
            instance.set_password(password)

        instance.save()

        # Set approvers, if changed
        if set(instance.approvers.all()) != set(approvers):
            instance.approvers.clear()
            for approver in approvers:
                instance.add_approver(approver)

        return instance
