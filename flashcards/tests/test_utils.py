from flashcards.utils import check_input


def test_check_input_correct():
    correct1 = check_input("かとう", "かとう")
    assert correct1 is True

    correct2 = check_input("たかばし", "たかはし,たかばし,こうきょう")
    assert correct2 is True


def test_check_input_incorrect():
    incorrect = check_input("たかば", "たかはし,たかばし,こうきょう")
    assert incorrect is False
