from django.contrib.auth.models import User

from flashcards.models import Deck, Flashcard, Review


def check_input(input_hiragana: str, expected_hiragana: str) -> bool:
    """Checks that the input is a correct answer.

    :param input_hiragana: the hiragana input by a user
    :param expected_hiragana: a string of the correct answers with each value separated by a comma
    :return: a boolean for if the answer is true or false
    """
    list_of_correct_answer = expected_hiragana.split(",")

    if input_hiragana in list_of_correct_answer:
        return True
    return False


def update_flashcards_in_deck(user_deck: Deck):
    """Updates the flashcards in a user's deck to determine if they are ready for review.

    :param user_deck: a Deck object containing the user's Reviews
    """
    reviews = list(Review.objects.filter(deck=user_deck))
    for review in reviews:
        review.is_ready_for_review()
        review.save()


def get_number_of_user_review_cards(current_user: User) -> int:
    """Gets the number of Review objects in a user's Deck.

    :param current_user: the user that is signed in
    :return: an integer representing the number of cards in a user's deck
    """
    user_deck = Deck.objects.filter(user=current_user).first()
    return Review.objects.filter(deck=user_deck, ready_for_review=True).count()


def get_number_of_user_learn_cards(current_user: User) -> int:
    """Gets the number of cards a user still has to learn.

    :param current_user: the user that is signed in
    :return: an integer representing the number of cards a user had left to learn
    """
    if user_deck := Deck.objects.filter(user=current_user).first():
        return Flashcard.objects.exclude(deck=user_deck.id).count()
    else:
        return Flashcard.objects.all().count()
