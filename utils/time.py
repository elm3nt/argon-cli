def get_time(content):
    hour =  re.search(r'real\t(.*?)h(.*?)m(.*?)s', content)
    if hour:
        hh = int(hour.group(1))

        min_sec = re.search(r'real\t[\d]*h(.*?)m(.*?)s', content)
        if min_sec:
            mm = int(min_sec.group(1))
            ss = int(min_sec.group(2).split('.')[0])
            ms = int(min_sec.group(2).split('.')[1])

            return (hh * 3600) + (mm * 60) + ss + (ms / 1000)

    else:
        min_sec = re.search(r'real\t(.*?)m(.*?)s', content)
        if min_sec:
            mm = int(min_sec.group(1))
            ss = int(min_sec.group(2).split('.')[0])
            ms = int(min_sec.group(2).split('.')[1])

            return (mm * 60) + ss + (ms / 1000)

    return 0
