def check_input(input_hiragana, expected_hiragana):
    list_of_correct_answer = expected_hiragana.split(",")

    if input_hiragana in list_of_correct_answer:
        return True
    return False
