'''Tigress module.'''
import re
import os

from utils import fs
from core.const import CMD, RE_OBFUSCATION, EXT, DIR_NAME, FILE_NAME
from tigress.const import ABSTRACT, TIGRESS_CMD, DATA, CONTROL_FLOW, \
                          VIRTUALIZATION, TIGRESS_REPLACE, VN, TIGRESS_RE


def obscure(input_path, output_path, obfuscation, file_name, index, v_n):
    '''
    Applies obfuscation techniques for any combination of ABSTRACT, DATA,
    CONTROL FLOW, and VIRTUALIZATION.

    Arguments:
        input_path {str} -- Non-obfuscated c file path
        output_path {str} -- Obfuscated c file path
        obfuscation {str} -- Obfuscatoin choice
        file_name {str} -- Name of the generated file
        index {str} -- The number of generated variants
        v_n {int} -- Vn

    Returns:
        str -- path of the newly generated c file to be used for next
                 obfuscation
    '''
    output_file_path = ''
    temp_c_file_1 = 'temp1.c'
    temp_c_file_2 = 'temp2.c'
    output_file = '{}{}.c'.format(file_name, index)

    if obfuscation == ABSTRACT:
        output_file_path_1 = os.path.join(
            output_path, file_name, temp_c_file_1)
        cmd_temp_1 = TIGRESS_CMD['abstract'].format(
            vn=v_n, output=output_file_path_1, input=input_path)
        os.system(CMD['bash'].format(cmd_temp_1))

        output_file_path_2 = os.path.join(
            output_path, file_name, temp_c_file_2)
        cmd_temp_2 = TIGRESS_CMD['abstract-2'].format(
            vn=v_n, output=output_file_path_2, input=output_file_path_1)
        os.system(CMD['bash'].format(cmd_temp_2))

        output_file_path = os.path.join(output_path, file_name, output_file)
        cmd = TIGRESS_CMD['abstract-3'].format(vn=v_n,
                                               output=output_file_path,
                                               input=output_file_path_2)
        os.system(CMD['bash'].format(cmd))

        os.remove(output_file_path_1)
        os.remove(output_file_path_2)

    elif obfuscation == CONTROL_FLOW:
        output_file_path = os.path.join(output_path, file_name, output_file)
        cmd = TIGRESS_CMD['control-flow'].format(
            vn=v_n, output=output_file_path, input=input_path)
        os.system(CMD['bash'].format(cmd))

    elif obfuscation == DATA:
        output_file_path = os.path.join(output_path, file_name, output_file)
        cmd = TIGRESS_CMD['data'].format(
            vn=v_n, output=output_file_path, input=input_path)
        os.system(CMD['bash'].format(cmd))

    elif obfuscation == VIRTUALIZATION:
        output_file_path = os.path.join(output_path, file_name, output_file)
        cmd = TIGRESS_CMD['virtualization'].format(
            vn=v_n, output=output_file_path, input=input_path)
        os.system(CMD['bash'].format(cmd))

    return output_file_path


def variant(
        original_input_path,
        output_path,
        obfuscation_combinations,
        no_of_variants=1):
    '''
    Iterates through the number of variatns and obfuscation list to generate the
    necessary output path and calls the obscure function.

    Arguments:
        original_input_path {str} -- Single non-obfuscated file path
        output_path {str} -- obfuscated c file path

    Keyword Arguments:
        obfuscation_combinations {dict} -- List of combinations of each
                                           obfuscation technique (default: {{}})
        no_of_variants {int} -- The number of variants to be generated (default: {1})
    '''
    for index in range(1, no_of_variants + 1):
        for combination in obfuscation_combinations:
            if re.search(RE_OBFUSCATION, combination):
                v_n = VN
                file_name = ''
                input_path = original_input_path

                for obfuscation in combination:
                    file_name += obfuscation
                    target_path = os.path.join(output_path, file_name)

                    fs.mkdir(target_path, False)

                    input_path = obscure(
                        input_path,
                        output_path,
                        obfuscation.upper(),
                        file_name,
                        str(index),
                        v_n)
                    v_n += 1


def generate(output_path, code, password):
    '''
    Generates a original c file with a code and/or password to be used for
    symbolic execution tools.

    Arguments:
        output_path {str} -- Generated c file path
        code {list} -- List of activation codes to implemented into the c file
        password {list} -- List of passwords to be implemented into the c file
    '''
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
        code_args = TIGRESS_REPLACE['num-code'].format(
            count=code_count)
        mega_init = TIGRESS_REPLACE['mega-init'].format(
            count=code_count + 1, count2=code_count)
        act_code = TIGRESS_REPLACE['code'].format(count=index)
        code_input = TIGRESS_REPLACE['input'].format(
            count=index, count2=index - 1)
        check_code = TIGRESS_REPLACE['check-code'].format(
            count=index, code=code[index - 1])
        randomfuns = TIGRESS_REPLACE['randfuns'].format(
            index=index, index2=index - 1)
        mod_file = re.sub(TIGRESS_RE['arg-code'], code_args, mod_file)
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
            TIGRESS_RE['one-nl'] + act_code,
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
    '''
    Iterates through each c file in a folder or just a single c file and
    calls the variant function.

    Arguments:
        input_path {str} -- Non-obfuscated c file/files path
        output_path {str} -- Obfuscated c file path
        obfuscation_combinations {list} -- the list of combinations of
                                           obfuscation techniques
        no_of_variants {int} -- The number of variants for each obfuscation
    '''
    input_files_path = fs.ls(input_path, EXT['c'])

    for input_path in input_files_path:
        input_file = fs.details(input_path)
        output_dir_path = os.path.join(output_path, input_file['name'])

        fs.mkdir(output_dir_path, False)

        variant(
            input_path,
            output_dir_path,
            obfuscation_combinations,
            no_of_variants)

        fs.rmdirs(output_dir_path, obfuscation_combinations)
