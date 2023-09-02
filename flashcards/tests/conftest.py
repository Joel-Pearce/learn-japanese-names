from flashcards.models import Flashcard, Review, Deck
from django.contrib.auth.models import User
import pytest
from datetime import datetime


@pytest.fixture
def flashcard():
    return Flashcard.objects.create(kanji="日", hiragana="にち")


@pytest.fixture
def user():
    return User.objects.create_user(
        username="example_user", password="Abc123!!!", email="example@test.com"
    )


@pytest.fixture
def deck(user, flashcard):
    deck = Deck.objects.create(user=user)
    deck.save()
    return deck


@pytest.fixture
def review(flashcard, user, deck):
    return Review.objects.create(
        deck=deck,
        flashcard=flashcard,
        last_review_date=datetime(1994, 9, 21),
        next_review_date=datetime(1994, 9, 21),
        ready_for_review=True,
    )
