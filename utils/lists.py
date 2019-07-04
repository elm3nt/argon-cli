import re


def has_string(pattern_list, content_list):
    for pattern in pattern_list:
        if pattern in ''.join(content_list):
            return True

    return False


def to_str_with_nl(array):
    return '\n'.join(array)
