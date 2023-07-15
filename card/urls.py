from django.urls import path
from .views import CardsView, create_card_view

urlpatterns = [
    path('cards/', CardsView.as_view(), name='card_list'),
    path('cards/create/', create_card_view, name='create_card_form'),
]





