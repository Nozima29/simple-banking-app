from django.contrib import admin
from cards.models import Card, CardHistory
# Register your models here.

admin.site.register(Card)
admin.site.register(CardHistory)
