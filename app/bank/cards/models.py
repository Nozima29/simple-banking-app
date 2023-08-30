from django.db import models
from cards import STATES, TYPES
from users.models import AuthUser

from datetime import datetime
import uuid
import logging
# Create your models here.

logger = logging.getLogger('card_logger')


class Card(models.Model):
    user = models.ForeignKey(AuthUser, on_delete=models.CASCADE)
    state = models.CharField(max_length=50, choices=STATES, default='active')
    type = models.CharField(max_length=50, choices=TYPES)
    last4 = models.CharField(max_length=10)
    exp_month = models.IntegerField()
    exp_year = models.IntegerField()
    cvv = models.IntegerField(default=123)
    cardholder_name = models.CharField(max_length=100, null=True)
    balance = models.FloatField()

    # custom token generation (in actual case should be done by special API gateway)
    token = models.UUIDField(default=uuid.uuid4, unique=True, editable=False)

    def withdraw_cash(self, amount):
        if amount < self.balance:
            self.balance -= amount
            logger.info("Amount is successfully withdrawn!")
        else:
            logger.error("Amount exceeds current balance!")
        self.save()

    def deposit_cash(self, amount):
        if self.is_valid:
            self.balance += amount
            self.save()
        else:
            logger.error("Card is ", self.state)

    def enable(self):
        if self.is_valid:
            self.state = 'active'
            self.save()
        else:
            logger.error("Card is ", self.state)

    def disable(self):
        self.state = 'inactive'
        self.save()

    def is_valid(self):
        now_year = datetime.now().year
        now_month = datetime.now().month
        exp_year = 2000 + self.exp_year
        if exp_year < now_year or \
                exp_year == now_year and self.exp_month < now_month:
            self.state = 'expired'
            self.save()
            return False
        else:
            return True

    @classmethod
    def register(self, user, name, number, exp_date, cvv):
        Card.objects.create(
            user=user,
            cardholder_name=name,
            last4=number[-4:],
            exp_month=exp_date[2:],
            exp_year=exp_date[-2:],
            cvv=cvv if int(cvv) else 123,
            balance=0.0,
            type='mastercard'
        )

    def __str__(self) -> str:
        return f"{self.user.user.email} - {self.type}"


class CardHistory(models.Model):
    card = models.ForeignKey(
        Card, on_delete=models.SET_NULL, related_name='card_history', null=True)
    saved_state = models.CharField(max_length=50, choices=STATES)
    deleted = models.BooleanField(default=False)

    def __str__(self) -> str:
        return f"{self.card.user} - {self.saved_state}"
