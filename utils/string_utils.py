import random

import string


def shorten_text(text, max_length):
    if len(text) <= max_length:
        return text
    else:
        return text[:max_length - 3] + "..."  # truncate text and add ellipsis


def isolate_string(isolation_string, input_string):
    if isolation_string not in input_string:
        return input_string

    first_string_index = input_string.index(isolation_string)
    return input_string[:first_string_index + 1].replace(isolation_string, '') + isolation_string + input_string[
                                                                                                    first_string_index + 1:].replace(
        isolation_string, '')


def generate_random_string(length, use_letters=True, use_digits=True, use_special_chars=False):
    characters = ''
    if use_letters:
        characters += string.ascii_letters
    if use_digits:
        characters += string.digits
    if use_special_chars:
        characters += string.punctuation

    if not characters:
        raise ValueError("No character set selected")

    return ''.join(random.choice(characters) for i in range(length))
