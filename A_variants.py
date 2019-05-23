#!/usr/bin/python

import os
import sys
from pathlib import Path

#--FilePrefix=v"{}"a 
CMD = {
    'bash': '/bin/bash -c "{}"',
    'compile': '''tigress \
				--Verbosity=1 \
				--Transform=Split \
				--Seed=0 \
				--SplitKinds=deep,block,top \
				--SplitCount=10 \
				--Functions=SECRET \
				--Transform=CleanUp \
				--CleanUpKinds=annotations \
				--out=A{}.c {} '''
	}


def compile(file_path):
	for i in range(1, 21):
		compile = CMD['compile'].format(i, file_path)
		print(compile)
		os.system(CMD['bash'].format(compile))
	


dir = sys.argv[1]

dir_list = Path(dir).glob('**/*.c')
for path in dir_list:
	file_path = str(path.absolute())
	print(file_path)
	#c_file = os.path.basename(file_path)
	
	
	compile(file_path)
