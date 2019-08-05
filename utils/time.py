'''Module for time operations.'''
import re


def get_time(content):
    '''
    Extract time frome time command ouput.

    Arguments:
        content {str} -- Time command output

    Returns:
        float -- Time in seconds
    '''
    time = 0
    hr_min_sec = re.search(r'real[\s]*(.*?)h(.*?)m(.*?)s', content)

    if hr_min_sec:
        hours = int(hr_min_sec.group(1))
        minutes = int(hr_min_sec.group(2))
        seconds = int(hr_min_sec.group(3))
        milliseconds = int(hr_min_sec.group(4))

        time = (hours * 3600) + (minutes * 60) + seconds + (milliseconds / 1000)

    else:
        min_sec = re.search(r'real[\s]*(.*?)m(.*?)\.(.*?)s', content)
        if min_sec:
            minutes = int(min_sec.group(1))
            seconds = int(min_sec.group(2))
            milliseconds = int(min_sec.group(3))

            time = (minutes * 60) + seconds + (milliseconds / 1000)

    return time
