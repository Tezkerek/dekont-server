from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK

from groups.permissions import IsInGroup, IsNotInGroup
from groups.serializers import GroupSerializer, GroupJoinSerializer
from groups.models import Group

from .serializers import UserSerializer, UserRegistrationSerializer
from .models import User

# Create your views here.

class RegistrationAPIView(APIView):
    """
    Registers a user.
    """
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)

        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        response_data = {'user': UserSerializer(user).data}

        return Response(data=response_data, status=HTTP_201_CREATED)

class UserViewSet(mixins.RetrieveModelMixin,
                  viewsets.GenericViewSet):

    lookup_field = 'pk'
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated]
    action_permission_classes = {
        'group': {
            'delete': permission_classes + [IsInGroup],
            'post': permission_classes + [IsNotInGroup]
        }
    }

    def get_queryset(self):
        # Only users in the same group
        user = self.request.user
        return User.objects.filter(group_id=user.group_id)

    def get_permissions(self):
        action_permission_classes = self.get_action_permission_classes()

        # Get the permissions classes for the action and method,
        # or the default ones if not defined.
        permission_classes = action_permission_classes \
            .get(self.action, {}) \
            .get(self.request.method.lower(), self.permission_classes)

        return [permission() for permission in permission_classes]

    def get_action_permission_classes(self):
        return getattr(self, 'action_permission_classes', {})

    @action(methods=['get', 'post', 'delete'], detail=True)
    def group(self, request, pk=None):
        """
        Acts on the user's group relation.
        """
        if request.method == 'POST':
            """
            Sets the user's group using the invite code (join group).
            """
            serializer = GroupJoinSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            invite_code = serializer.validated_data['invite_code']
            group = get_object_or_404(Group, invite_code=invite_code)

            request.user.group = group
            request.user.save()

            return Response(status=HTTP_200_OK)

        elif request.method == 'DELETE':
            """
            Unsets the user's group (leave group).
            """
            request.user.group = None
            request.user.save()

            return Response(status=HTTP_200_OK)
