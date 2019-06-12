#!/usr/bin/python

import os
import sys
import shutil

from pathlib import Path

VN = 1
ALL_DIRS = 1
RENDUNDANT_DIRS = 2
ABSTRACT = 'A'
VIRTUALIZATION = 'V'
CONTROL_FLOW = 'C'
DATA = 'D'


CMD = {
    'bash': '/bin/bash -c "{}"'
}

OBFUSCATION = {
    'abstract': 'tigress \
		--Verbosity=1 \
		--FilePrefix=v{vn}a \
		--Transform=Split \
		--Seed=0 \
		--SplitKinds=deep,block,top \
		--SplitCount=10 \
		--Functions=SECRET \
		--Transform=CleanUp \
		--CleanUpKinds=annotations \
		--out={output} {input}',

	'abstract-2': '''tigress \
		--FilePrefix=v{vn}b \
		--Verbosity=1  \
		--Transform=RndArgs \
		--Seed=0 \
		--RndArgsBogusNo=2?5 \
				''' + "--Functions=_v{vn}a_1_SECRET_SECRET_split_1"
				+ ",_v{vn}a_1_SECRET_SECRET_split_2"
				+ ",_v{vn}a_1_SECRET_SECRET_split_3"
				+ ",_v{vn}a_1_SECRET_SECRET_split_4"
				+ ",_v{vn}a_1_SECRET_SECRET_split_5"
				+ ",_v{vn}a_1_SECRET_SECRET_split_6"
				+ ",_v{vn}a_1_SECRET_SECRET_split_7"
				+ ",_v{vn}a_1_SECRET_SECRET_split_8"
				+ ",_v{vn}a_1_SECRET_SECRET_split_9"
				+ ",_v{vn}a_1_SECRET_SECRET_split_10 " +
'''--Transform=CleanUp \
		--CleanUpKinds=annotations \
		--out={output} {input}''',

	'abstract-3': '''tigress --Verbosity=1   \
		--FilePrefix=v{vn} \
		--Transform=InitEntropy \
		--Functions=main  \
		--Transform=InitOpaque \
		--Functions=main \
		--InitOpaqueCount=2 \
		--InitOpaqueStructs=list,array  \
				--Transform=Merge \
				''' + "--Functions=_v{vn}a_1_SECRET_SECRET_split_1"
				+ ",_v{vn}a_1_SECRET_SECRET_split_2"
				+ ",_v{vn}a_1_SECRET_SECRET_split_3"
				+ ",_v{vn}a_1_SECRET_SECRET_split_4"
				+ ",_v{vn}a_1_SECRET_SECRET_split_5"
				+ ",_v{vn}a_1_SECRET_SECRET_split_6"
				+ ",_v{vn}a_1_SECRET_SECRET_split_7"
				+ ",_v{vn}a_1_SECRET_SECRET_split_8"
				+ ",_v{vn}a_1_SECRET_SECRET_split_9"
				+ ",_v{vn}a_1_SECRET_SECRET_split_10 " +
		'''--Transform=CleanUp \
		--CleanUpKinds=annotations \
		--out={output} {input}''',

	'control-flow': 'tigress \
		--Verbosity=1 \
		--FilePrefix=v{vn} \
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
		--out={output} {input}',
	
	'data': 'tigress \
		--Verbosity=1  \
		--FilePrefix=v{vn} \
		--Transform=InitEntropy \
		--Functions=main  \
		--Transform=EncodeLiterals \
		--Functions=SECRET  \
		--Transform=CleanUp \
		--CleanUpKinds=annotations \
		--out={output} {input}',

	'virtualization': 'tigress \
		--Verbosity=1  \
		--FilePrefix=v{vn} \
		--Transform=Virtualize \
		--Functions=SECRET \
		--VirtualizeDispatch=switch \
		--Transform=CleanUp \
		--CleanUpKinds=annotations \
		--out={output} {input}'
	}


def obfuscate(input_path, output_path, obfuscation, file_name, index, vn):
	temp_c_file_1 = 'temp1.c'
	temp_c_file_2 = 'temp2.c'
	output_file = '{}{}.c'.format(file_name, index)
	output_file_path = ''
	print(input_path, output_path, obfuscation, file_name, index, vn)
	if obfuscation == ABSTRACT:
		output_file_path_1 = os.path.join(output_path, file_name, temp_c_file_1)
		cmd_temp_1 = OBFUSCATION['abstract'].format(vn = vn, output = output_file_path_1, input = input_path)
		os.system(CMD['bash'].format(cmd_temp_1))

		output_file_path_2 = os.path.join(output_path, file_name, temp_c_file_2)
		cmd_temp_2 = OBFUSCATION['abstract-2'].format(vn = vn, output = output_file_path_2, input = output_file_path_1)
		os.system(CMD['bash'].format(cmd_temp_2))


		output_file_path = os.path.join(output_path, file_name, output_file)
		cmd = OBFUSCATION['abstract-3'].format(vn = vn, output = output_file_path, input = output_file_path_2)
		os.system(CMD['bash'].format(cmd))
	
		os.remove(output_file_path_1) 
		os.remove(output_file_path_2)

	elif obfuscation == CONTROL_FLOW:
		output_file_path = os.path.join(output_path, file_name, output_file)
		cmd = OBFUSCATION['control-flow'].format(vn = vn, output = output_file_path, input = input_path)
		os.system(CMD['bash'].format(cmd))

	elif obfuscation == DATA:
		output_file_path = os.path.join(output_path, file_name, output_file)
		cmd = OBFUSCATION['data'].format(vn = vn, output = output_file_path, input = input_path)
		os.system(CMD['bash'].format(cmd))

	elif obfuscation == VIRTUALIZATION:
		output_file_path = os.path.join(output_path, file_name, output_file)
		cmd = OBFUSCATION['virtualization'].format(vn = vn, output = output_file_path, input = input_path)
		os.system(CMD['bash'].format(cmd))

	return output_file_path


def clean_up(path, option, core_dirs = {}):
	dir_list = os.listdir(path)

	for dir in dir_list:
		target_path = os.path.join(path, dir)

		if option == ALL_DIRS and os.path.isdir(target_path):
			shutil.rmtree(target_path)
		elif option == RENDUNDANT_DIRS and dir not in core_dirs:
			shutil.rmtree(target_path)


def variant(input_path, output_path, obfuscation_combinations = {}, no_of_variants = 1):
	for index in range(1, no_of_variants + 1):
		for combination in obfuscation_combinations:
			vn = VN
			file_name = ''
			
			for obfuscation in combination:
				file_name += obfuscation
				target_path = os.path.join(output_path, file_name)

				if not os.path.isdir(target_path):
					os.mkdir(target_path)

				new_path = obfuscate(input_path, output_path, obfuscation.upper(), file_name, str(index), vn)

				vn += 1
				input_file_path = new_path


dir = sys.argv[1]
if __name__ == '__main__':
	obfuscation_combinations = {'A', 'ADC'}
	input_path = os.path.abspath(sys.argv[1])
	output_path = os.path.abspath(sys.argv[2]) 
	no_of_variants = int(sys.argv[3])
	
	clean_up(output_path, ALL_DIRS)

	variant(input_path, output_path, obfuscation_combinations, no_of_variants)

	clean_up(output_path, RENDUNDANT_DIRS, obfuscation_combinations)
