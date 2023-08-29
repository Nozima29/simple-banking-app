from django.shortcuts import render
from django.contrib.auth.models import User
from users.models import AuthUser
from cards.models import Card, CardHistory
# Create your views here.


def register(request):
    template = 'cards/main.html'
    auth_user = AuthUser.objects.filter(user=request.user).first()
    cards = Card.objects.filter(user=auth_user)
    context = {'cards': cards}
    print(cards)
    if request.POST:
        name = request.POST.get('name', None)
        number = request.POST.get('number', None)
        exp_date = request.POST.get('exp_date', None)
        cvv = request.POST.get('cvv', None)
        Card.register(auth_user, name, number, exp_date, cvv)

    return render(request, template, context)


def deposit_cash(request):
    pass


def withdraw_cash(request):
    pass
