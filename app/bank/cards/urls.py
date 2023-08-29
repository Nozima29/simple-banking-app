from django.urls import path
from cards.views import *

app_name = 'cards'
urlpatterns = [
    path('', register, name='register')
]
