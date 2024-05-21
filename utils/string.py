def shorten_text(text, max_length):
    if len(text) <= max_length:
        return text
    else:
        return text[:max_length - 3] + "..."  # truncate text and add ellipsis


def remove_all_but_one_zero(s):
    if '0' not in s:
        return s

    first_zero_index = s.index('0')
    return s[:first_zero_index + 1].replace('0', '') + '0' + s[first_zero_index + 1:].replace('0', '')
