from datetime import datetime

from flashcards.models import Flashcard, Review, Deck
from django.contrib.auth.models import User
import pytest


@pytest.fixture
def flashcard():
    return Flashcard.objects.create(kanji="日", hiragana="にち")


@pytest.fixture
def user():
    return User.objects.create(username="example_user", password="Abc123!!!")


@pytest.fixture
def deck(user, flashcard):
    deck = Deck.objects.create(user=user)
    deck.flashcards.add(flashcard)
    return deck


@pytest.fixture
def review(flashcard, user, deck):
    return Review.objects.create(
        deck=deck,
        flashcard=flashcard,
        last_review_date=datetime(1994, 9, 21),
        next_review_date=datetime(1994, 9, 21),
        ready_for_review=False,
    )


@pytest.mark.django_db
def test_flashcard_model(flashcard):
    assert str(flashcard) == "日"


@pytest.mark.django_db
def test_user_model(user):
    assert user.username == "example_user"


@pytest.mark.django_db
def test_deck_model(deck):
    assert deck.user.username == "example_user"


@pytest.mark.django_db
def test_review_model(review):
    assert review.ready_for_review is False
    review.is_ready_for_review()
    assert review.ready_for_review is True

    assert review.next_review_date == datetime(1994, 9, 21)
    review.update_review_date(True)
    assert review.next_review_date > datetime(1994, 9, 21)
    current_review_data = review.next_review_date
    review.update_review_date(False)
    assert current_review_data != review.next_review_date
