#!/usr/bin/python

import os
import sys
import shutil
from pathlib import Path

#all combinations 
combi = {'A', 'ACD', 'ACDV', 'ADC', 'ADCV', 'C', 'CAD', 'CADV', 'CDA', 'CDAV'}

#tigress commands
CMD = {
    'bash': '/bin/bash -c "{}"',

    'compileA': '''tigress \
				--Verbosity=1 \
				--FilePrefix=v{}a \
				--Transform=Split \
				--Seed=0 \
				--SplitKinds=deep,block,top \
				--SplitCount=10 \
				--Functions=SECRET \
				--Transform=CleanUp \
				--CleanUpKinds=annotations \
				--out={}1A.c {} ''',

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
				--out={d}2A.c {s}''',

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
				--out={d}{n}{num}.c {s}''',

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
def compile(case, dir, file_path, file_num, name, vn):
	if case == 'A':
		compileA = CMD['compileA'].format(vn, dir + name + '/', file_path)
		os.system(CMD['bash'].format(compileA))
		src = os.path.abspath(dir + name + '/1A.c')
		compileA2 = CMD['compileA2'].format(a = vn, d = dir + name + '/', s = src)
		os.system(CMD['bash'].format(compileA2))
		src2 = os.path.abspath(dir + name + '/2A.c')
		compileA3 = CMD['compileA3'].format(a = vn, d = dir + name + '/', n = name, num = file_num, s = src2)
		os.system(CMD['bash'].format(compileA3))
		os.remove(src) 
		os.remove(src2)
	elif case == 'C':
		compileC = CMD['compileC'].format(a = vn, d = dir + name + '/', n = name, num = file_num, s = file_path)
		os.system(CMD['bash'].format(compileC))
	elif case == 'D':
		compileD = CMD['compileD'].format(vn, dir + name + '/', name, file_num, file_path)
		os.system(CMD['bash'].format(compileD))
	elif case == 'V':
		compileV = CMD['compileV'].format(vn, dir + name + '/', name, file_num, file_path)
		os.system(CMD['bash'].format(compileV))

	return os.path.abspath(dir + name + '/' + name + str(file_num) + '.c')

#clears out folders in directory
def CleanUp(option):
	folder_list = os.listdir(dir)
	if option == 1:
		for folder in folder_list:
			if os.path.isdir(dir + folder):
				shutil.rmtree(dir + folder)
	elif option == 2:
		for folder in folder_list:
			if len(folder) == 2:
				shutil.rmtree(dir + folder)

def Variants(combinations, file_num):
	for combo in combinations:
		path = os.path.abspath(dir + 'original.c')
		file_name = ''
		vn = 1
		for char in combo:
			file_name += char
			if os.path.isdir(dir + file_name):
				pass
			else:
				os.mkdir(dir + file_name)
			new_path = compile(char, dir, path, file_num, file_name, vn)
			vn += 1
			path = new_path

#main
dir = sys.argv[1]

#cleans directory
CleanUp(1)

#creates the 20 variants
for i in range(1, 21):
	Variants(combi, i)

CleanUp(2)
