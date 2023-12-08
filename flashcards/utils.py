from flashcards.models import Deck, Flashcard, Review


def check_input(input_hiragana, expected_hiragana):
    list_of_correct_answer = expected_hiragana.split(",")

    if input_hiragana in list_of_correct_answer:
        return True
    return False


def update_flashcards_in_deck(user_deck):
    reviews = list(Review.objects.filter(deck=user_deck))
    for review in reviews:
        review.is_ready_for_review()
        review.save()


def get_number_of_user_review_cards(current_user):
    user_deck = Deck.objects.filter(user=current_user).first()
    return Review.objects.filter(deck=user_deck, ready_for_review=True).count()


def get_number_of_user_learn_cards(current_user):
    if user_deck := Deck.objects.filter(user=current_user).first():
        return Flashcard.objects.exclude(deck=user_deck.id).count()
    else:
        return Flashcard.objects.all().count()
