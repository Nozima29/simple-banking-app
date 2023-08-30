import pytest
from cards.models import Card
from users.models import AuthUser
from django.contrib.auth.models import User
# Create your tests here.


@pytest.fixture
def register_card():
    def make_card(**kwargs):
        user = User.objects.create(username="test_user", password="12333")
        auth_user = AuthUser.objects.create(user=user)
        kwargs.update({"user": auth_user})
        return Card.register(**kwargs)
    return make_card


@pytest.mark.django_db
def test_register_card(register_card):
    register_card(
        name="test",
        number="12345678910",
        exp_date="1225",
        cvv="123"
    )
    assert Card.objects.all().count() == 1
    assert Card.objects.get(cardholder_name="test") is not None


@pytest.mark.django_db
def test_card_deposit(register_card):
    register_card(
        name="test",
        number="12345678910",
        exp_date="1225",
        cvv="123"
    )
    card = Card.objects.get(cardholder_name="test")
    card.deposit_cash(100)
    assert card.balance == 100


@pytest.mark.django_db
def test_card_withdraw(register_card):
    register_card(
        name="test",
        number="12345678910",
        exp_date="1225",
        cvv="123"
    )
    card = Card.objects.get(cardholder_name="test")
    card.balance = 100
    card.save()
    card.withdraw_cash(50)
    assert card.balance == 50


@pytest.mark.django_db
def test_card_is_valid(register_card):
    register_card(
        name="test",
        number="12345678910",
        exp_date="1224",
        cvv="123"
    )
    card = Card.objects.get(cardholder_name="test")
    assert card.is_valid() == True


@pytest.mark.django_db
def test_card_is_not_valid(register_card):
    register_card(
        name="test",
        number="12345678910",
        exp_date="1222",
        cvv="123"
    )
    card = Card.objects.get(cardholder_name="test")
    assert card.is_valid() == False
    assert card.state == "expired"


@pytest.mark.django_db
def test_card_enable(register_card):
    register_card(
        name="test",
        number="12345678910",
        exp_date="1223",
        cvv="123"
    )
    card = Card.objects.get(cardholder_name="test")
    card.enable()
    assert card.state == "active"


@pytest.mark.django_db
def test_card_disable(register_card):
    register_card(
        name="test",
        number="12345678910",
        exp_date="1223",
        cvv="123"
    )
    card = Card.objects.get(cardholder_name="test")
    card.disable()
    assert card.state == "inactive"
