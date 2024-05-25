def shorten_text(text, max_length):
    if len(text) <= max_length:
        return text
    else:
        return text[:max_length - 3] + "..."  # truncate text and add ellipsis


def isolate_string(isolation_string, input_string):
    if isolation_string not in input_string:
        return input_string

    first_string_index = input_string.index(isolation_string)
    return input_string[:first_string_index + 1].replace(isolation_string, '') + isolation_string + input_string[first_string_index + 1:].replace(isolation_string, '')
