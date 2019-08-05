'''Module for list operations.'''


def has_string(pattern_list, content_list):
    '''
    Check strings of list contains in another list of strings.

    Arguments:
        pattern_list {list} -- List of strings that needs to be compared
        content_list {list} -- List of strings that is compared with pattern

    Returns:
        bool -- Does pattern strings consists in content strings
    '''
    for pattern in pattern_list:
        if pattern in ''.join(content_list):
            return True

    return False


def to_str_with_nl(array):
    '''
    Convert list to string by joining by new line.

    Arguments:
        array {list} -- List of strings

    Returns:
        str -- List of string joined by new linw
    '''
    return '\n'.join(array)
