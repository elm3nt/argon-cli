#!/usr/bin/python3

import os
import re
import sys
import csv
import datetime
from pathlib import Path


def get_time(content):
    hour =  re.search(r'real\t(.*?)h(.*?)m(.*?)s', content)
    if hour:
        hh = int(hour.group(1))

        min_sec = re.search(r'real\t[\d]*h(.*?)m(.*?)s', content)
        if min_sec:
            mm = int(min_sec.group(1))
            ss = int(min_sec.group(2).split('.')[0])
            ms = int(min_sec.group(2).split('.')[1])

            return {'hh': hh, 'mm': mm, 'ss': ss, 'ms': ms}

    else:
        min_sec = re.search(r'real\t(.*?)m(.*?)s', content)
        if min_sec:
            mm = int(min_sec.group(1))
            ss = int(min_sec.group(2).split('.')[0])
            ms = int(min_sec.group(2).split('.')[1])

            return {'hh': 0, 'mm': mm, 'ss': ss, 'ms': ms}

    return None


if __name__ == '__main__':

    if len(sys.argv) != 2:
        print('Usage: analysis [test directory]')
        sys.exit(1)

    test_dir = sys.argv[1]
    data = [ ['File', 'Time taken', 'File size (in bytes)', 'Path'] ]

    test_dir_path_list = Path(test_dir).glob('**/*.time.txt')
    for path in test_dir_path_list:
        result_file_path = str(path.absolute())
        result_file = os.path.basename(result_file_path)

        with open(result_file_path, 'r') as content_file:
            content = content_file.read()

            time = get_time(content)
            if time is not None:
                time_taken = datetime.timedelta(hours = time['hh'], minutes = time['mm'], seconds = time['ss'], milliseconds = time['ms'])
            else:
                time_taken = '#error'

            c_file = result_file.replace('.time.txt', '.c')
            c_file_path = result_file_path.replace('.time.txt', '.c')
            file_size = os.path.getsize(c_file_path)
            data.append([c_file, str(time_taken), file_size, os.path.dirname(result_file_path)])

    analysis_file_path = os.path.join(test_dir, 'analysis.csv')
    with open(analysis_file_path, 'w') as analysis_file:
        writer = csv.writer(analysis_file)
        writer.writerows(data)
