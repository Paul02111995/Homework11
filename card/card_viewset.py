from rest_framework import viewsets, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.exceptions import ObjectDoesNotExist
from .models import Card
from .serializer import CardSerializer
from .permissions import IsOwner


class CardViewSet(viewsets.ModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    permission_classes = [permissions.IsAuthenticated, IsOwner]

    def list(self, request, *args, **kwargs):
        cards = Card.objects.filter(owner=request.user)
        serializer = self.get_serializer(cards, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        try:
            card = Card.objects.get(pk=pk, owner=request.user)
        except ObjectDoesNotExist:
            return Response({"error": "Card not found or you don't have access."}, status=status.HTTP_404_NOT_FOUND)
        serializer = self.get_serializer(card)
        return Response(serializer.data)

    def create(self, request, *args, **kwargs):
        request.data["owner"] = request.user.id
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def update(self, request, pk=None, *args, **kwargs):
        try:
            card = Card.objects.get(pk=pk, owner=request.user)
        except ObjectDoesNotExist:
            return Response({"error": "Card not found or you don't have access."}, status=status.HTTP_404_NOT_FOUND)
        if 'cvv' in request.data:
            card.cvv = request.data['cvv']
        if 'status' in request.data:
            card.status = request.data['status']
        card.save()
        serializer = self.get_serializer(card)
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def freeze(self, request, pk=None):
        try:
            card = Card.objects.get(pk=pk, owner=request.user)
        except ObjectDoesNotExist:
            return Response({"error": "Card not found or you don't have access."}, status=status.HTTP_404_NOT_FOUND)

        if card.status == 'active':
            card.status = 'frozen'
            card.save()
            return Response({"message": "Card has been frozen."})
        else:
            return Response({"message": "Card cannot be frozen as it is not in Active status."},
                            status=status.HTTP_400_BAD_REQUEST)

    @action(detail=True, methods=["post"])
    def unfreeze(self, request, pk=None):
        try:
            card = Card.objects.get(pk=pk, owner=request.user)
        except ObjectDoesNotExist:
            return Response({"error": "Card not found or you don't have access."}, status=status.HTTP_404_NOT_FOUND)

        if card.status == 'frozen':
            card.status = 'active'
            card.save()
            return Response({"message": "Card has been unfrozen."})
        else:
            return Response({"message": "Card cannot be unfrozen as it is not in Frozen status."},
                            status=status.HTTP_400_BAD_REQUEST)