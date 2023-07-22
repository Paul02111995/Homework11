from django.db import models
import uuid
from django.contrib.auth.models import User

class Card(models.Model):
    STATUS_CHOICES = (
        ('new', 'New'),
        ('active', 'Active'),
        ('blocked', 'Blocked'),
        ('frozen', 'Frozen'),
    )
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    pan = models.CharField(max_length=16)
    expiry_date = models.CharField(max_length=5)
    cvv = models.CharField(max_length=3)
    issue_date = models.DateField()
    owner = models.ForeignKey(User, on_delete=models.CASCADE, default=None)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='new')

    objects = models.Manager()

    def __str__(self):
        return f"Card ID: {self.id}, PAN: {self.pan}, Expiry Date: {self.expiry_date}, CVV: {self.cvv}, Issue Date: {self.issue_date}, Owner ID: {self.owner_id}, Owner: {self.owner}, Status: {self.status}"
