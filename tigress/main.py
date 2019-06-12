
import os
import sys
import shutil
from pathlib import Path

from .const import *
from core.const import *


def obfuscate(input_path, output_path, obfuscation, file_name, index, vn):
    output_file_path = ''
    temp_c_file_1 = 'temp1.c'
    temp_c_file_2 = 'temp2.c'
    output_file = '{}{}.c'.format(file_name, index)

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

                obfuscate(input_path, output_path, obfuscation.upper(), file_name, str(index), vn)
                vn += 1


def task(input_path, output_path, obfuscation_combinations, no_of_variants):
    clean_up(output_path, ALL_DIRS)
    variant(input_path, output_path, obfuscation_combinations, no_of_variants)
    clean_up(output_path, RENDUNDANT_DIRS, obfuscation_combinations)
