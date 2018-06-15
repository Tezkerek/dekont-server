from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.status import HTTP_201_CREATED

from .serializers import UserSerializer, UserRegistrationSerializer

# Create your views here.

class RegistrationAPIView(APIView):
    """
    Registers a user.
    """
    permission_classes = (AllowAny,)
    serializer_class = UserRegistrationSerializer

    def post(self, request):
        user_data = request.data.get('user', {})
        serializer = self.serializer_class(data=user_data)

        if serializer.is_valid(raise_exception=True):
            serializer.save()

        response_data = {'user': serializer.validated_data}

        return Response(data=response_data, status=HTTP_201_CREATED)
