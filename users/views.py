from rest_framework.views import APIView
from rest_framework import viewsets, mixins
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import exceptions
from rest_framework.status import HTTP_201_CREATED, HTTP_200_OK
from django.utils.translation import ugettext_lazy as _

from .serializers import (
    UserSerializer,
    UserRegistrationSerializer,
    GroupSerializer
)
from .permissions import IsInGroup, IsNotInGroup
from .models import User, Group

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
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        # Only users in the same group
        user = self.request.user
        return User.objects.filter(group_id=user.group_id)

    @action(methods=['get'], detail=True)
    def group(self, request, pk=None):
        """
        Retrieves the user's group.
        """
        context = {'request': self.request}
        serializer = GroupSerializer(self.get_object().group, context=context)
        return Response(data=serializer.data)

class GroupViewSet(viewsets.GenericViewSet):
    """
    A ViewSet for actions on groups.
    """
    permission_classes = (IsAuthenticated,)
    serializer_class = GroupSerializer

    queryset = Group.objects.all()

    def get_permissions(self):
        permission_classes = [IsAuthenticated]

        if self.action == 'create':
            permission_classes.append(IsNotInGroup)

        return [permission() for permission in permission_classes]

    def get_serializer_context(self):
        return {'request': self.request}

    def create(self, request):
        # Validate and save
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        group = serializer.save(group_admin=request.user)

        # Serialize and respond
        serializer = self.serializer_class(group)
        response_data = {'group': serializer.data}

        return Response(data=response_data, status=HTTP_201_CREATED)

    @action(methods=['post'], detail=True, permission_classes=[IsNotInGroup])
    def join(self, request, pk=None):
        invite_code = pk
        user = request.user

        group = Group.objects.get(invite_code=invite_code)
        user.group = group
        user.save()

        return Response(status=HTTP_200_OK)

    @action(methods=['post'], detail=False, permission_classes=[IsAuthenticated, IsInGroup])
    def leave(self, request):
        request.user.group = None
        request.user.save()

        return Response(status=HTTP_200_OK)
