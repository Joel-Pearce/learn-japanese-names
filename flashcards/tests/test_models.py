from datetime import datetime
import pytest


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
    review.ready_for_review = False
    review.save()
    review.is_ready_for_review()
    assert review.ready_for_review is True

    assert review.next_review_date == datetime(1994, 9, 21)
    review.update_review_date(True)
    assert review.next_review_date > datetime(1994, 9, 21)
    current_review_data = review.next_review_date
    review.update_review_date(False)
    assert current_review_data != review.next_review_date
