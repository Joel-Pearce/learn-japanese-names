import pytest

from flashcards.models import Review
from flashcards.utils import (
    check_input,
    update_flashcards_in_deck,
    get_number_of_user_review_cards,
    get_number_of_user_learn_cards,
)


def test_check_input_correct():
    correct1 = check_input("かとう", "かとう")
    assert correct1 is True

    correct2 = check_input("たかばし", "たかはし,たかばし,こうきょう")
    assert correct2 is True


def test_check_input_incorrect():
    incorrect = check_input("たかば", "たかはし,たかばし,こうきょう")
    assert incorrect is False


@pytest.mark.django_db
def test_update_flashcards(
    user, flashcard, deck_with_reviewable_flashcard, review_to_be_updated
):
    review = Review.objects.filter(deck=deck_with_reviewable_flashcard).first()
    assert review.ready_for_review is False

    update_flashcards_in_deck(deck_with_reviewable_flashcard)
    review = Review.objects.filter(deck=deck_with_reviewable_flashcard).first()
    assert review.ready_for_review is True


@pytest.mark.django_db
def test_get_number_of_user_review_learn_cards_single_user(
    flashcard, multiple_flashcards, user, deck, review
):
    num_to_review = get_number_of_user_review_cards(user)
    assert num_to_review == 1

    num_to_learn = get_number_of_user_learn_cards(user)
    assert num_to_learn == 3


@pytest.mark.django_db
def test_get_number_of_user_review_learn_cards_multiple_users(
    flashcard, multiple_flashcards, multiple_users, multiple_decks, multiple_reviews
):
    num_to_review = get_number_of_user_review_cards(multiple_users[0])
    assert num_to_review == 3

    num_to_learn = get_number_of_user_learn_cards(multiple_users[0])
    assert num_to_learn == 1
