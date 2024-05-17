from freezegun import freeze_time

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
    assert review.next_review_date >= review.last_review_date

    review.ready_for_review = False
    review.save()
    review.is_ready_for_review()
    assert review.ready_for_review is True

    old_last_review_date = review.last_review_date
    old_next_review_date = review.next_review_date
    review.update_review_date(True)
    assert review.last_review_date > old_last_review_date
    assert review.next_review_date > old_next_review_date

    old_last_review_date = review.last_review_date
    old_next_review_date = review.next_review_date
    review.update_review_date(False)
    assert review.last_review_date == old_last_review_date
    assert review.next_review_date == old_next_review_date


@pytest.mark.django_db
def test_review_time_increments(review):
    assert review.exponential_time == 1
    assert review.exponential_increment == 0
    review.update_review_date(True)
    assert review.exponential_time == 2
    assert review.exponential_increment == 1
    review.update_review_date(True)
    assert review.exponential_time == 4
    assert review.exponential_increment == 2
    review.update_review_date(True)
    assert review.exponential_time == 7
    assert review.exponential_increment == 3

    difference_in_time = review.next_review_date - review.last_review_date
    assert difference_in_time.days == 4

    review.update_review_date(False)
    assert review.exponential_time == 7

    review.update_review_date(True)
    assert review.exponential_time == 4
    assert review.exponential_increment == 0


@pytest.mark.django_db
def test_review_is_ready_when_time_passes(review):
    review.update_review_date(True)
    assert review.ready_for_review is False

    with freeze_time("21-09-2094"):
        review.is_ready_for_review()
        assert review.ready_for_review is True
