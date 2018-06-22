from rest_framework import parsers, renderers
from rest_framework.compat import coreapi, coreschema
from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK
from rest_framework.schemas import ManualSchema
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import Token
from .serializers import ObtainTokenSerializer
from .utils import get_username_field

class ObtainAuthToken(APIView):
    throttle_classes = ()
    permission_classes = ()
    parser_classes = (parsers.FormParser, parsers.MultiPartParser, parsers.JSONParser,)
    renderer_classes = (renderers.JSONRenderer,)
    serializer_class = ObtainTokenSerializer

    def __init__(self):
        # Define schema dynamically, in order to use User.USERNAME_FIELD
        if coreapi is not None and coreschema is not None:
            User = get_user_model()
            USERNAME_FIELD = get_username_field()

            self.schema = ManualSchema(
                fields=[
                    coreapi.Field(
                        name=USERNAME_FIELD,
                        required=True,
                        location='form',
                        schema=coreschema.String(
                            title=USERNAME_FIELD.capitalize(),
                            description="Valid {} for authentication".format(USERNAME_FIELD),
                        ),
                    ),
                    coreapi.Field(
                        name="password",
                        required=True,
                        location='form',
                        schema=coreschema.String(
                            title="Password",
                            description="Valid password for authentication",
                        ),
                    ),
                ],
                encoding="application/json",
            )

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)

        user = serializer.validated_data['user']
        name = serializer.validated_data['name']

        token, created = Token.objects.get_or_create(user=user, name=name)
        return Response({'token': token.key})

class InvalidateAuthToken(APIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        if request.auth:
            request.auth.delete()
        return Response(status=HTTP_200_OK)

obtain_auth_token = ObtainAuthToken.as_view()
invalidate_auth_token = InvalidateAuthToken.as_view()
