from num2words import num2words


def number_in_words(value, lang="en_IN"):
    number_in_words = num2words(int(value), lang=lang)
    number_in_words = (
        str(number_in_words).replace("-", " ").title().replace("And", "and")
    )
    return number_in_words
