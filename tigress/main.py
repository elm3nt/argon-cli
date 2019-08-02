
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
        output_file_path_1 = os.path.join(
            output_path, file_name, temp_c_file_1)
        cmd_temp_1 = TIGRESS_CMD['abstract'].format(
            vn=vn, output=output_file_path_1, input=input_path)
        os.system(CMD['bash'].format(cmd_temp_1))

        output_file_path_2 = os.path.join(
            output_path, file_name, temp_c_file_2)
        cmd_temp_2 = TIGRESS_CMD['abstract-2'].format(
            vn=vn, output=output_file_path_2, input=output_file_path_1)
        os.system(CMD['bash'].format(cmd_temp_2))

        output_file_path = os.path.join(output_path, file_name, output_file)
        cmd = TIGRESS_CMD['abstract-3'].format(vn=vn,
                                               output=output_file_path,
                                               input=output_file_path_2)
        os.system(CMD['bash'].format(cmd))

        os.remove(output_file_path_1)
        os.remove(output_file_path_2)

    elif obfuscation == CONTROL_FLOW:
        output_file_path = os.path.join(output_path, file_name, output_file)
        cmd = TIGRESS_CMD['control-flow'].format(
            vn=vn, output=output_file_path, input=input_path)
        os.system(CMD['bash'].format(cmd))

    elif obfuscation == DATA:
        output_file_path = os.path.join(output_path, file_name, output_file)
        cmd = TIGRESS_CMD['data'].format(
            vn=vn, output=output_file_path, input=input_path)
        os.system(CMD['bash'].format(cmd))

    elif obfuscation == VIRTUALIZATION:
        output_file_path = os.path.join(output_path, file_name, output_file)
        cmd = TIGRESS_CMD['virtualization'].format(
            vn=vn, output=output_file_path, input=input_path)
        os.system(CMD['bash'].format(cmd))

    return output_file_path


def variant(
        original_input_path,
        output_path,
        obfuscation_combinations={},
        no_of_variants=1):
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

                    input_path = obscure(
                        input_path,
                        output_path,
                        obfuscation.upper(),
                        file_name,
                        str(index),
                        vn)
                    vn += 1


def generate(output_path, code, password):
    code_count = len(code)
    password_count = len(password)
    input_path = os.path.join(
        os.path.dirname(
            os.path.realpath(__file__)),
        '..',
        DIR_NAME['samples'],
        FILE_NAME['empty-c-file'])

    if code[0] is not None and password[0] is None:
        activation_code = TIGRESS_CMD['code'].format(code=code[0])
        cmd = TIGRESS_CMD['generate'].format(
            option=activation_code, output=output_path, input=input_path)
    elif code[0] is None and password[0] is not None:
        code_count = 0
        passwd = TIGRESS_CMD['pass'].format(password=password[0])
        cmd = TIGRESS_CMD['generate'].format(
            option=passwd, output=output_path, input=input_path)
    elif code[0] is not None and password[0] is not None:
        activation_code = TIGRESS_CMD['code'].format(code=code[0])
        passwd = TIGRESS_CMD['pass'].format(password=password[0])
        cmd = TIGRESS_CMD['generate'].format(option=' '.join(
            [passwd, activation_code]), output=output_path, input=input_path)

    os.system(CMD['bash'].format(cmd))
    mod_file = fs.read(output_path)

    if not code_count:
        replace = TIGRESS_REPLACE['while'].format(count=code_count)
        mod_file = re.sub(TIGRESS_RE['while-random-funs'], replace, mod_file)
        mega_init = TIGRESS_REPLACE['mega-init'].format(
            count=code_count + 1, count2=code_count)
        mod_file = re.sub(TIGRESS_RE['argc-nl'], mega_init, mod_file)

    for index in range(password_count, 1, -1):
        pas = TIGRESS_REPLACE['pass'].format(count=index)
        printf = TIGRESS_REPLACE['printf'].format(count=index)

        check_pass = TIGRESS_REPLACE['check-pass'].format(
            count=index, password=password[index - 1])
        mod_file = re.sub(
            TIGRESS_RE['char-password'],
            TIGRESS_RE['one-nl'] + pas,
            mod_file)
        mod_file = re.sub(
            TIGRESS_RE['printf-please'],
            TIGRESS_RE['one-nl'] + printf,
            mod_file)
        mod_file = re.sub(
            TIGRESS_RE['string-compare-result'],
            TIGRESS_RE['one-nl'] +
            check_pass,
            mod_file)

    for index in range(code_count, 1, -1):
        mega_init = TIGRESS_REPLACE['mega-init'].format(
            count=code_count + 1, count2=code_count)
        ac = TIGRESS_REPLACE['code'].format(count=index)
        code_input = TIGRESS_REPLACE['input'].format(
            count=index, count2=index - 1)
        check_code = TIGRESS_REPLACE['check-code'].format(
            count=index, code=code[index - 1])
        randomfuns = TIGRESS_REPLACE['randfuns'].format(
            index=index, index2=index - 1)
        mod_file = re.sub(TIGRESS_RE['argc-nl'], mega_init, mod_file)
        mod_file = re.sub(
            TIGRESS_RE['random-funs-value'],
            TIGRESS_RE['one-nl'] +
            randomfuns,
            mod_file)
        mod_file = re.sub(
            TIGRESS_RE['int-activation-code'],
            TIGRESS_REPLACE['unsigned-long-activation-code'],
            mod_file)
        mod_file = re.sub(
            TIGRESS_RE['unsigned-long-activation-code'],
            TIGRESS_RE['one-nl'] + ac,
            mod_file)
        mod_file = re.sub(
            TIGRESS_RE['activation-code'],
            TIGRESS_RE['one-nl'] +
            code_input,
            mod_file)
        mod_file = re.sub(
            TIGRESS_RE['failed'],
            TIGRESS_RE['one-nl'] +
            check_code,
            mod_file)

    fs.write(output_path, mod_file)


def obfuscate(
        input_path,
        output_path,
        obfuscation_combinations,
        no_of_variants):
    input_files_path = fs.ls(input_path, EXT['c'])

    for input_path in input_files_path:
        input_file = fs.details(input_path)
        output_dir_path = os.path.join(output_path, input_file['name'])

        fs.mkdir(output_dir_path)

        variant(
            input_path,
            output_dir_path,
            obfuscation_combinations,
            no_of_variants)

        fs.rmdirs(output_dir_path, obfuscation_combinations)
