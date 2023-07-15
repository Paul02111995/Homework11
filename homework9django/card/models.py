from django.db import models
import uuid

class Card(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pan = models.CharField(max_length=16)
    expiry_date = models.CharField(max_length=5)
    cvv = models.CharField(max_length=3)
    issue_date = models.DateField()
    owner_id = models.CharField(max_length=9)
    status = models.CharField(max_length=10)

    objects = models.Manager()

    def is_valid(self):
        card_number = self.pan.replace(" ", "").replace("-", "")

        if len(card_number) < 13 or len(card_number) > 19:
            return False

        if not card_number.isdigit():
            return False

        digits = [int(x) for x in card_number]
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]

        total = sum(odd_digits)
        for digit in even_digits:
            doubled_digit = digit * 2
            if doubled_digit > 9:
                doubled_digit -= 9
            total += doubled_digit

        return total % 10 == 0

    def __str__(self):
        return f"Card ID: {self.id}, PAN: {self.pan}, Expiry Date: {self.expiry_date}, Owner ID: {self.owner_id}"
