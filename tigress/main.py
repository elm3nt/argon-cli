
import os
import sys
import shutil
from pathlib import Path

from .const import *
from utils import file
from core.const import *


def obscure(input_path, output_path, obfuscation, file_name, index, vn):
    output_file_path = ''
    temp_c_file_1 = 'temp1.c'
    temp_c_file_2 = 'temp2.c'
    output_file = '{}{}.c'.format(file_name, index)

    if obfuscation == ABSTRACT:
        output_file_path_1 = os.path.join(output_path, file_name, temp_c_file_1)
        cmd_temp_1 = TIGRESS_CMD['abstract'].format(vn = vn, output = output_file_path_1, input = input_path)
        os.system(CMD['bash'].format(cmd_temp_1))

        output_file_path_2 = os.path.join(output_path, file_name, temp_c_file_2)
        cmd_temp_2 = TIGRESS_CMD['abstract-2'].format(vn = vn, output = output_file_path_2, input = output_file_path_1)
        os.system(CMD['bash'].format(cmd_temp_2))

        output_file_path = os.path.join(output_path, file_name, output_file)
        cmd = TIGRESS_CMD['abstract-3'].format(vn = vn, output = output_file_path, input = output_file_path_2)
        os.system(CMD['bash'].format(cmd))

        os.remove(output_file_path_1)
        os.remove(output_file_path_2)

    elif obfuscation == CONTROL_FLOW:
        output_file_path = os.path.join(output_path, file_name, output_file)
        cmd = TIGRESS_CMD['control-flow'].format(vn = vn, output = output_file_path, input = input_path)
        os.system(CMD['bash'].format(cmd))

    elif obfuscation == DATA:
        output_file_path = os.path.join(output_path, file_name, output_file)
        cmd = TIGRESS_CMD['data'].format(vn = vn, output = output_file_path, input = input_path)
        os.system(CMD['bash'].format(cmd))

    elif obfuscation == VIRTUALIZATION:
        output_file_path = os.path.join(output_path, file_name, output_file)
        cmd = TIGRESS_CMD['virtualization'].format(vn = vn, output = output_file_path, input = input_path)
        os.system(CMD['bash'].format(cmd))

    return output_file_path


def variant(original_input_path, output_path, obfuscation_combinations = {}, no_of_variants = 1):
    for index in range(1, no_of_variants + 1):
        for combination in obfuscation_combinations:
            vn = VN
            file_name = ''
            input_path = original_input_path

            for obfuscation in combination:
                file_name += obfuscation
                target_path = os.path.join(output_path, file_name)

                if not os.path.isdir(target_path):
                    os.mkdir(target_path)

                input_path = obscure(input_path, output_path, obfuscation.upper(), file_name, str(index), vn)
                vn += 1


def generate(output_path, code = '18', password = 'p@$$w0rd'):
    input_path = os.path.join(os.getcwd(), DIR_NAME['samples'], FILE_NAME['empty-c-file'])
    cmd = TIGRESS_CMD['generate'].format(password = password, code = code, output = output_path, input = input_path)
    print(cmd)
    os.system(CMD['bash'].format(cmd))


def obfuscate(input_path, output_path, obfuscation_combinations, no_of_variants):
    variant(input_path, output_path, obfuscation_combinations, no_of_variants)
    file.remove_dirs_except(output_path, obfuscation_combinations)
