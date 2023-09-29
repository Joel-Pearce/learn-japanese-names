from flashcards.models import Review


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
