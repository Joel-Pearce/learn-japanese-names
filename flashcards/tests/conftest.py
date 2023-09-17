from flashcards.models import Flashcard, Review, Deck
from django.contrib.auth.models import User
import pytest
from datetime import datetime
from django.contrib.auth.hashers import make_password


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


@pytest.fixture
def multiple_flashcards():
    flashcards = [
        Flashcard(kanji="日", hiragana="にち"),
        Flashcard(kanji="⼝", hiragana="くち"),
        Flashcard(kanji="去", hiragana="きょ"),
    ]
    Flashcard.objects.bulk_create(flashcards)
    return flashcards


@pytest.fixture
def multiple_users():
    users = [
        User(
            username="example_user1",
            password=make_password("Abc123!!!"),
            email="example1@test.com",
        ),
        User(
            username="example_user2",
            password=make_password("Abc123!!!"),
            email="example2@test.com",
        ),
        User(
            username="example_user3",
            password=make_password("Abc123!!!"),
            email="example3@test.com",
        ),
    ]
    User.objects.bulk_create(users)
    return users


@pytest.fixture
def multiple_decks(multiple_users, multiple_flashcards):
    decks = []
    for user in multiple_users:
        deck = Deck.objects.create(user=user)
        deck.save()
        decks.append(deck)
    return decks


@pytest.fixture
def multiple_reviews(multiple_decks, multiple_flashcards):
    reviews = []
    for deck in multiple_decks:
        for flashcard in multiple_flashcards:
            review = Review.objects.create(
                deck=deck,
                flashcard=flashcard,
                last_review_date=datetime(1994, 9, 21),
                next_review_date=datetime(1994, 9, 21),
                ready_for_review=True,
            )
            reviews.append(review)
    return reviews
