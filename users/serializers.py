from rest_framework import serializers
from rest_framework.compat import authenticate
from rest_framework.reverse import reverse
from django.utils.translation import ugettext_lazy as _

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

class UserSerializer(serializers.ModelSerializer):
    group = serializers.HyperlinkedRelatedField(view_name='user-group', read_only=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    class Meta:
        model = User
        fields = ('id', 'email', 'password', 'username', 'group', 'parent', 'is_group_admin')
        extra_kwargs = {'password': {'write_only': True}}

    def update(self, instance, validated_data):
        # Password is not set with setattr()
        password = validated_data.pop('password', None)

        # Update attributes
        for (key, value) in validated_data.items():
            setattr(instance, key, value)

        # Set password properly
        if password is not None:
            instance.set_password(password)

        instance.save()

        return instance
