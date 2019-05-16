#!/usr/bin/python3

import os
import re
import sys
import datetime
from pathlib import Path


if len(sys.argv) < 2:
    print('Usage: batch [test directory]')
    sys.exit(1)

root_dir = sys.argv[1]


SYM_STDIN = "--sym-stdin 12"
pathlist = Path(root_dir).glob('**/*.time.txt')
BASH = '/bin/bash -c "{}"'
for path in pathlist:
    result_file_path = str(path.absolute())
    result_file = os.path.basename(result_file_path)
    test_file_name = result_file.replace('.time.txt', '')

    with open(result_file_path, 'r') as content_file:
        content = content_file.read()
       	hour =  re.search(r'real\t(.*?)h(.*?)m(.*?)s', content)
        if hour:
            hh = int(hour.group(1))
            
            min_sec = re.search(r'real\t[\d]*h(.*?)m(.*?)s', content)
            if min_sec:
                mm = int(min_sec.group(1))
                ss = int(min_sec.group(2).split('.')[0])
                ms = int(min_sec.group(2).split('.')[1])

            time_taken = datetime.timedelta(hours = hh, minutes = mm, seconds = ss, milliseconds = ms)
        else:
            min_sec = re.search(r'real\t(.*?)m(.*?)s', content)
            if min_sec:
                mm = int(min_sec.group(1))
                ss = int(min_sec.group(2).split('.')[0])
                ms = int(min_sec.group(2).split('.')[1])
        
                time_taken = datetime.timedelta(hours = 0, minutes = mm, seconds = ss, milliseconds = ms)

        print(test_file_name, os.path.dirname(result_file_path), str(time_taken), os.path.getsize(result_file_path))


