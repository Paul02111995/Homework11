from django.test import TestCase, Client
from django.urls import reverse

from .models import Card
import uuid


class CardTestCase(TestCase):
    def setUp(self):
        self.client = Client()

    def test_get_card_list_empty(self):
        url = reverse("card_list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "cards/card_list.html")
        self.assertContains(response, "There are no cards yet")

    def test_card_list_view(self):
        Card.objects.create(pan="4111111111111111", expiry_date="12/25", cvv="123", issue_date="2022-01-01", owner_id="123456789", status="Active")
        Card.objects.create(pan="5555555555554444", expiry_date="12/23", cvv="456", issue_date="2022-01-01", owner_id="987654321", status="Inactive")

        response = self.client.get(reverse("card_list"))

        self.assertEqual(response.status_code, 200)

        self.assertContains(response, "4111111111111111")
        self.assertContains(response, "5555555555554444")

    def test_create_card_view(self):

        response = self.client.post(reverse("create_card_form"), {
            "pan": "4111111111111111",
            "expiry_date": "12/25",
            "cvv": "123",
            "issue_date": "2022-01-01",
            "owner_id": "123456789",
            "status": "Active"
        })

        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, reverse("card_list"))


        self.assertEqual(Card.objects.count(), 1)
        card = Card.objects.first()
        self.assertEqual(card.pan, "4111111111111111")

    def test_card_is_valid(self):
        card = Card(
            pan="4111111111111111",
            expiry_date="12/23",
            cvv="123",
            issue_date="2022-01-01",
            owner_id="ABC123XYZ",
            status="active"
        )
        self.assertTrue(card.is_valid())

    def test_card_is_not_valid(self):
        card = Card(
            pan="4111111111111112",
            expiry_date="12/23",
            cvv="123",
            issue_date="2022-01-01",
            owner_id="ABC123XYZ",
            status="active"
        )
        self.assertFalse(card.is_valid())

    def test_card_is_not_valid_short_number(self):
        card = Card(
            pan="1234",
            expiry_date="12/23",
            cvv="123",
            issue_date="2022-01-01",
            owner_id="ABC123XYZ",
            status="active"
        )
        self.assertFalse(card.is_valid())

    def test_card_is_not_valid_long_number(self):
        card = Card(
            pan="41111111111111112222",
            expiry_date="12/23",
            cvv="123",
            issue_date="2022-01-01",
            owner_id="ABC123XYZ",
            status="active"
        )
        self.assertFalse(card.is_valid())

    def test_card_is_not_valid_non_numeric_number(self):
        card = Card(
            pan="411111111111111a",
            expiry_date="12/23",
            cvv="123",
            issue_date="2022-01-01",
            owner_id="ABC123XYZ",
            status="active"
        )
        self.assertFalse(card.is_valid())

    def test_card_is_valid_with_dashes(self):
        card = Card(
            pan="4111-1111-1111-1111",
            expiry_date="12/23",
            cvv="123",
            issue_date="2022-01-01",
            owner_id="ABC123XYZ",
            status="active"
        )
        self.assertTrue(card.is_valid())