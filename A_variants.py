#!/usr/bin/python

import os
import sys
import shutil

from pathlib import Path

VN = 1
ALL_DIRS = 1
RENDUNDANT_DIRS = 2
NO_OF_VARIANTS = 20
RENDUNDANT_DIR_LENGTH = 2
INPUT_FILE = 'original.c'
ABSCTRACT = 'A'
VIRTUALIZATION = 'V'
CONTROL_FLOW = 'C'
DATA = 'D'

#all combinations 
COMBINATIONS = {'A', 'ACD', 'ACDV', 'ADC', 'ADCV', 'C', 'CAD', 'CADV', 'CDA', 'CDAV'}

#tigress commands
CMD = {
    'bash': '/bin/bash -c "{}"',

    'compileA': '''tigress \
				--Verbosity=1 \
				--FilePrefix=v{v}a \
				--Transform=Split \
				--Seed=0 \
				--SplitKinds=deep,block,top \
				--SplitCount=10 \
				--Functions=SECRET \
				--Transform=CleanUp \
				--CleanUpKinds=annotations \
				--out={output}/1A.c {input} ''',

	'compileA2': '''tigress \
				--FilePrefix=v{a}b \
				--Verbosity=1  \
				--Transform=RndArgs \
				--Seed=0 \
				--RndArgsBogusNo=2?5 \
				''' + "--Functions=_v{a}a_1_SECRET_SECRET_split_1"
				+ ",_v{a}a_1_SECRET_SECRET_split_2"
				+ ",_v{a}a_1_SECRET_SECRET_split_3"
				+ ",_v{a}a_1_SECRET_SECRET_split_4"
				+ ",_v{a}a_1_SECRET_SECRET_split_5"
				+ ",_v{a}a_1_SECRET_SECRET_split_6"
				+ ",_v{a}a_1_SECRET_SECRET_split_7"
				+ ",_v{a}a_1_SECRET_SECRET_split_8"
				+ ",_v{a}a_1_SECRET_SECRET_split_9"
				+ ",_v{a}a_1_SECRET_SECRET_split_10 " +
				'''--Transform=CleanUp \
				--CleanUpKinds=annotations \
				--out={d}/2A.c {s}''',

	'compileA3': '''tigress --Verbosity=1   \
				--FilePrefix=v{a} \
				--Transform=InitEntropy \
				--Functions=main  \
				--Transform=InitOpaque \
				--Functions=main \
				--InitOpaqueCount=2 \
				--InitOpaqueStructs=list,array  \
				--Transform=Merge \
				''' + "--Functions=_v{a}a_1_SECRET_SECRET_split_1"
				+ ",_v{a}a_1_SECRET_SECRET_split_2"
				+ ",_v{a}a_1_SECRET_SECRET_split_3"
				+ ",_v{a}a_1_SECRET_SECRET_split_4"
				+ ",_v{a}a_1_SECRET_SECRET_split_5"
				+ ",_v{a}a_1_SECRET_SECRET_split_6"
				+ ",_v{a}a_1_SECRET_SECRET_split_7"
				+ ",_v{a}a_1_SECRET_SECRET_split_8"
				+ ",_v{a}a_1_SECRET_SECRET_split_9"
				+ ",_v{a}a_1_SECRET_SECRET_split_10 " +
				'''--Transform=CleanUp \
				--CleanUpKinds=annotations  \
				--out={d}/{n}{num}.c {s}''',

	'compileC': 'tigress \
				--Verbosity=1 \
				--FilePrefix=v{a} \
				--Transform=InitOpaque \
				--Functions=main \
				--Transform=UpdateOpaque \
				--Functions=SECRET \
				--UpdateOpaqueCount=10 \
				--Transform=AddOpaque \
				--Functions=SECRET \
				--AddOpaqueCount=10  \
				--AddOpaqueKinds=call,bug,true,junk \
				--Transform=Flatten \
				--Functions=SECRET \
				-FlattenObfuscateNext=true \
				--FlattenDispatch=switch \
				--Transform=CleanUp \
				--CleanUpKinds=annotations \
				--out={d}{n}{num}.c {s}',
	
	'compileD': '''tigress \
				--Verbosity=1  \
				--FilePrefix=v{} \
				--Transform=InitEntropy \
				--Functions=main  \
				--Transform=EncodeLiterals \
				--Functions=SECRET  \
				--Transform=CleanUp \
				--CleanUpKinds=annotations \
				--out={}{}{}.c {}''',

	'compileV': '''tigress \
				--Verbosity=1  \
				--FilePrefix=v{} \
				--Transform=Virtualize \
				--Functions=SECRET \
				--VirtualizeDispatch=switch \
				--Transform=CleanUp \
				--CleanUpKinds=annotations \
				--out={}{}{}.c {}'''
	}

#compilation of Abstract, controlflow, data, and virtualization
def compile(obfuscation, path, file_path, file_num, file_name, vn):

	file_path = os.path.join(path, file_name)

	if obfuscation == ABSCTRACT:
		compileA = CMD['compileA'].format(v = vn, output = file_path, input = file_name)
		os.system(CMD['bash'].format(compileA))

		src = os.path.abspath(path + file_name + '1A.c')
		compileA2 = CMD['compileA2'].format(a = vn, d = file_path, s = src)
		os.system(CMD['bash'].format(compileA2))

		src2 = os.path.abspath(path + file_name + '2A.c')
		compileA3 = CMD['compileA3'].format(a = vn, d = file_path, n = file_name, num = file_num, s = src2)
		os.system(CMD['bash'].format(compileA3))
	
		os.remove(src) 
		os.remove(src2)
	elif obfuscation == CONTROL_FLOW:
		compileC = CMD['compileC'].format(a = vn, d = path + file_name + '/', n = file_name, num = file_num, s = file_path)
		os.system(CMD['bash'].format(compileC))
	elif obfuscation == DATA:
		compileD = CMD['compileD'].format(vn, path + file_name + '/', file_name, file_num, file_path)
		os.system(CMD['bash'].format(compileD))
	elif obfuscation == VIRTUALIZATION:
		compileV = CMD['compileV'].format(vn, path + file_name + '/', file_name, file_num, file_path)
		os.system(CMD['bash'].format(compileV))

	return os.path.abspath(path + file_name + '/' + file_name + str(file_num) + '.c')

def clean_up(path, option):
	dir_list = os.listdir(path)

	for dir in dir_list:
		target_path = os.path.join(path, dir)

		if option == ALL_DIRS and os.path.isdir(target_path):
			shutil.rmtree(target_path)
		elif option == RENDUNDANT_DIRS and len(dir) == RENDUNDANT_DIR_LENGTH:
			shutil.rmtree(target_path)

def variant(path, input_file, combinations, index):
	for combination in combinations:
		input_file_path = os.path.join(path, input_file)

		vn = VN
		file_name = ''
		for obfuscation in combination:
			file_name += obfuscation
			target_path = os.path.join(path, file_name)

			if not os.path.isdir(target_path):
				os.mkdir(target_path)

			new_path = compile(obfuscation, path+'/', input_file_path, index, file_name, vn)

			vn += 1
			input_file_path = new_path

#main


dir = sys.argv[1]
if __name__ == '__main__':
	output_path = os.path.abspath(sys.argv[1])

	clean_up(output_path, ALL_DIRS)

	for i in range(1, NO_OF_VARIANTS + 1):
		variant(output_path, INPUT_FILE, COMBINATIONS, i)

	clean_up(2)


Java
thisIsAVariable
ThisIsAClass

Python
this_is_a_variable
ThisClass