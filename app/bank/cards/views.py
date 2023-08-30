from django.shortcuts import render, redirect
from django.urls import reverse
from django.contrib import messages
from users.models import AuthUser
from cards.models import Card
# Create your views here.


def register(request):
    template = 'cards/main.html'
    user_request = request.POST
    if not request.user:
        return redirect(reverse('users:login'))
    auth_user = AuthUser.objects.filter(user=request.user).first()
    cards = Card.objects.filter(user=auth_user)
    context = {'cards': cards}

    if user_request and not user_request.get('deposit', None) and \
            not user_request.get('withdraw', None) and \
            not user_request.get('check', None):
        name = user_request.get('name', None)
        number = user_request.get('number', None)
        exp_date = user_request.get('exp_date', None)
        cvv = user_request.get('cvv', None)
        if name and number and exp_date:
            Card.register(auth_user, name, number, exp_date, cvv)
    else:
        actions(request)

    return render(request, template, context)


def actions(request):
    user_request = request.POST
    deposit = user_request.get('deposit', None)
    withdraw = user_request.get('withdraw', None)
    card = user_request.get('check', None)
    if user_request:
        if not card:
            messages.add_message(request, messages.INFO, "No card selected!")
        elif card and deposit and not withdraw:
            deposit_cash(deposit, card)
        elif card and withdraw and not deposit:
            withdraw_cash(withdraw, card)
        elif card and withdraw and deposit:
            messages.add_message(request, messages.INFO,
                                 "Cannot process both actions!")
        elif card and not deposit and not withdraw:
            messages.add_message(request, messages.INFO,
                                 "No input for Card actions!")
    return redirect(reverse('cards:register'))


def deposit_cash(amount, card):
    card_ = Card.objects.get(id=card)
    card_.deposit_cash(float(amount))


def withdraw_cash(amount, card):
    card_ = Card.objects.get(id=card)
    card_.withdraw_cash(float(amount))
