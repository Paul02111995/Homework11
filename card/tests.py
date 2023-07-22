from django.test import TestCase
from django.contrib.auth import get_user_model
from rest_framework.test import APIRequestFactory, force_authenticate
from rest_framework.test import APIClient
from rest_framework import status
from .models import Card
from .card_viewset import CardViewSet
class CardModelTests(TestCase):
    def setUp(self):
        self.factory = APIRequestFactory()
        self.view = CardViewSet.as_view({'get': 'retrieve'})
        self.user = get_user_model().objects.create_user(
            username='testuser',
            password='testpass',
        )
        self.other_user = get_user_model().objects.create_user(
            username='otheruser',
            password='otherpass',
        )

    def test_create_card(self):
        data = {
            "pan": "1111222233334444",
            "expiry_date": "12/25",
            "cvv": "123",
            "issue_date": "2023-07-21",
            "status": "active",
            "owner": self.user,
        }

        card = Card.objects.create(**data)
        self.assertEqual(Card.objects.count(), 1)
        self.assertEqual(card.owner, self.user)

    def test_list_cards(self):
        data1 = {
            "pan": "1111222233334444",
            "expiry_date": "12/25",
            "cvv": "123",
            "issue_date": "2023-07-21",
            "status": "active",
            "owner": self.user,
        }
        data2 = {
            "pan": "5555666677778888",
            "expiry_date": "06/24",
            "cvv": "456",
            "issue_date": "2023-07-21",
            "status": "active",
            "owner": self.user,
        }
        Card.objects.create(**data1)
        Card.objects.create(**data2)

        user_cards = Card.objects.filter(owner=self.user)

        self.assertEqual(user_cards.count(), 2)

    def test_retrieve_card(self):
        data = {
            "pan": "1111222233334444",
            "expiry_date": "12/25",
            "cvv": "123",
            "issue_date": "2023-07-21",
            "status": "active",
            "owner": self.user,
        }

        card = Card.objects.create(**data)
        retrieved_card = Card.objects.get(id=card.id)

        self.assertEqual(retrieved_card, card)
    def test_update_card(self):
        data = {
            "pan": "1111222233334444",
            "expiry_date": "12/25",
            "cvv": "123",
            "issue_date": "2023-07-21",
            "status": "active",
            "owner": self.user,
        }
        card = Card.objects.create(**data)

        new_data = {
            "pan": "9999888877776666",
            "expiry_date": "03/28",
            "cvv": "789",
            "issue_date": "2023-07-21",
            "status": "active",
            "owner": self.user,
        }

        card.pan = new_data["pan"]
        card.expiry_date = new_data["expiry_date"]
        card.cvv = new_data["cvv"]
        card.save()

        updated_card = Card.objects.get(id=card.id)

        self.assertEqual(updated_card.pan, new_data["pan"])
        self.assertEqual(updated_card.expiry_date, new_data["expiry_date"])
        self.assertEqual(updated_card.cvv, new_data["cvv"])
    def test_freeze_card(self):
        data = {
            "pan": "1111222233334444",
            "expiry_date": "12/25",
            "cvv": "123",
            "issue_date": "2023-07-21",
            "status": "active",
            "owner": self.user,
        }
        card = Card.objects.create(**data)
        card.status = "frozen"
        card.save()
        self.assertEqual(card.status, "frozen")
    def test_unfreeze_card(self):
        data = {
            "pan": "1111222233334444",
            "expiry_date": "12/25",
            "cvv": "123",
            "issue_date": "2023-07-21",
            "status": "frozen",
            "owner": self.user,
        }
        card = Card.objects.create(**data)
        card.status = "active"
        card.save()

        self.assertEqual(card.status, "active")
    def test_unauthorized_card_access(self):
        data = {
            "pan": "1111222233334444",
            "expiry_date": "12/25",
            "cvv": "123",
            "issue_date": "2023-07-21",
            "status": "active",
            "owner": self.other_user,
        }
        card = Card.objects.create(**data)

        request = self.factory.get(f'/cards/{card.id}/')
        force_authenticate(request, user=self.user)
        response = self.view(request, pk=card.id)

        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data, {"error": "Card not found or you don't have access."})

    def test_freeze_blocked_card(self):
        data = {
            "pan": "9999888877776666",
            "expiry_date": "03/28",
            "cvv": "789",
            "issue_date": "2023-07-21",
            "status": "blocked",
            "owner": self.user,
        }
        card = Card.objects.create(**data)

        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(f"/card/{card.id}/freeze/")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"message": "Card cannot be frozen as it is not in Active status."})

        card.refresh_from_db()
        self.assertEqual(card.status, "blocked")

    def test_freeze_frozen_card(self):
        data = {
            "pan": "9999888877776666",
            "expiry_date": "03/28",
            "cvv": "789",
            "issue_date": "2023-07-21",
            "status": "frozen",
            "owner": self.user,
        }
        card = Card.objects.create(**data)

        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(f"/card/{card.id}/freeze/")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"message": "Card cannot be frozen as it is not in Active status."})

        card.refresh_from_db()
        self.assertEqual(card.status, "frozen")

    def test_unfreeze_no_frozen_card(self):
        data = {
            "pan": "9999888877776666",
            "expiry_date": "03/28",
            "cvv": "789",
            "issue_date": "2023-07-21",
            "status": "active",
            "owner": self.user,
        }
        card = Card.objects.create(**data)

        client = APIClient()
        client.force_authenticate(user=self.user)
        response = client.post(f"/card/{card.id}/unfreeze/")

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data, {"message": "Card cannot be unfrozen as it is not in Frozen status."})

        card.refresh_from_db()
        self.assertEqual(card.status, "active")
