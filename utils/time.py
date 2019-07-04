import re


def get_time(content):
    hr_min_sec =  re.search(r'real[\s]*(.*?)h(.*?)m(.*?)s', content)
    if hr_min_sec:
        hh = int(hr_min_sec.group(1))
        mm = int(hr_min_sec.group(2))
        ss = int(hr_min_sec.group(3))
        ms = int(hr_min_sec.group(4))

        return (hh * 3600) + (mm * 60) + ss + (ms / 1000)

    else:
        min_sec = re.search(r'real[\s]*(.*?)m(.*?)\.(.*?)s', content)
        if min_sec:
            mm = int(min_sec.group(1))
            ss = int(min_sec.group(2))
            ms = int(min_sec.group(3))

            return (mm * 60) + ss + (ms / 1000)

    return 0
