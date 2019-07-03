import re


def has_string(arrs1, arrs2):
    for arr1 in arrs1:
        has_string = re.search(arr1, ''.join(arrs2))
        if has_string:
            return True

    return False
