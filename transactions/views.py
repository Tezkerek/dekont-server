from rest_framework import viewsets, mixins
from rest_framework.permissions import IsAuthenticated

from .serializers import TransactionSerializer

class TransactionViewSet(mixins.ListModelMixin,
                         mixins.RetrieveModelMixin,
                         mixins.CreateModelMixin,
                         mixins.UpdateModelMixin,
                         viewsets.GenericViewSet):

    lookup_field = 'pk'
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only user's transactions
        user = self.request.user
        user_transactions = user.transactions.all()

        return user_transactions
