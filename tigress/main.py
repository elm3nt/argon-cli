
import re
import os
import sys
import shutil
from pathlib import Path

from .const import *
from utils import fs
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
            if re.search(RE_OBFUSCATION, combination):
                vn = VN
                file_name = ''
                input_path = original_input_path

                for obfuscation in combination:
                    file_name += obfuscation
                    target_path = os.path.join(output_path, file_name)

                    fs.mkdir(target_path)

                    input_path = obscure(input_path, output_path, obfuscation.upper(), file_name, str(index), vn)
                    vn += 1


def generate(output_path, code, password):
    code_count = len(code)
    password_count = len(password)
    input_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), '..',
                              DIR_NAME['samples'], FILE_NAME['empty-c-file'])

    if code[0] != None and password[0] == None:
        activation_code = TIGRESS_CMD['code'].format(code = code[0])
        cmd = TIGRESS_CMD['generate'].format(option = activation_code, output = output_path, input = input_path)
    elif code[0] == None and password[0] != None:
        code_count = 0
        passwd = TIGRESS_CMD['pass'].format(password = password[0])
        cmd = TIGRESS_CMD['generate'].format(option = passwd, output = output_path, input = input_path)
    else:
        activation_code = TIGRESS_CMD['code'].format(code = code[0])
        passwd = TIGRESS_CMD['pass'].format(password = password[0])
        cmd = TIGRESS_CMD['generate'].format(option = ' '.join([passwd, activation_code]), output = output_path, input = input_path)

    os.system(CMD['bash'].format(cmd))
    mod_file = fs.read(output_path)

    if code_count == 0:
        replace = TIGRESS_REGREX['while'].format(count = code_count)
        mod_file = re.sub(r'while \(randomFuns_i5.*', replace, mod_file)
        megaint = TIGRESS_REGREX['megaint'].format(count = code_count + 1, count2 = code_count)
        mod_file = re.sub(r'argc !=.* {\n.*', megaint, mod_file)

    if code_count > 1 or password_count > 1:
        for index in range(password_count, 1, -1):
            pas = TIGRESS_REGREX['pass'].format(count = index)
            printf = TIGRESS_REGREX['printf'].format(count = index)

            check_pass = TIGRESS_REGREX['check_pass'].format(count = index, password = password[index - 1])
            mod_file = re.sub(r'(char password\[100\].*)', r'\1\n' + pas, mod_file)
            mod_file = re.sub(r'(printf\("Please.*\n  scanf\("%s", password\);)', r'\1\n' + printf, mod_file)
            mod_file = re.sub(r'(stringCompareResult = strncmp\(password,.*\n.*)', r'\1\n' + check_pass, mod_file)

        for index in range(code_count, 1, -1):
            megaint = TIGRESS_REGREX['megaint'].format(count = code_count + 1, count2 = code_count)
            ac = TIGRESS_REGREX['code'].format(count = index)
            code_input = TIGRESS_REGREX['input'].format(count = index, count2 = index - 1)
            check_code = TIGRESS_REGREX['check_code'].format(count = index, code = code[index - 1])
            randomfuns = TIGRESS_REGREX['randfuns'].format(index = index, index2 = index - 1)

            mod_file = re.sub(r'argc !=.* {\n.*', megaint, mod_file)
            mod_file = re.sub(r'(randomFuns_value6 =.*\n    input\[randomFuns_i5\].*)', r'\1\n' + randomfuns, mod_file )
            mod_file = re.sub(r'int activationCode ;', 'unsigned long activationCode ;', mod_file)
            mod_file = re.sub(r'(unsigned long activationCode ;)', r'\1\n' + ac, mod_file)
            mod_file = re.sub(r'(activationCode =.*)', r'\1\n' + code_input, mod_file)
            mod_file = re.sub(r'(failed \|= activationCode !.*)', r'\1\n' + check_code, mod_file)

    fs.write(output_path, mod_file)


def obfuscate(input_path, output_path, obfuscation_combinations, no_of_variants):
    input_files_path = fs.ls(input_path, EXT['c'])

    for input_path in input_files_path:
        input_file = fs.details(input_path)
        output_dir_path = os.path.join(output_path, input_file['name'])

        fs.mkdir(output_dir_path)

        variant(input_path, output_dir_path, obfuscation_combinations, no_of_variants)

        fs.rmdirs(output_dir_path, obfuscation_combinations)



