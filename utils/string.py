def shorten_text(text, max_length):
    if len(text) <= max_length:
        return text
    else:
        return text[:max_length - 3] + "..."  # truncate text and add ellipsis
