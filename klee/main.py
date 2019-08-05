'''Klee module for symbolic exection.'''
import os
import re

from utils import fs
from utils import lists
from klee.const import KLEE_CMD, KLEE_RE
from core.const import CMD, EXT, FILE_NAME


def compile_to_bytecode(input_file_path, output_file_path):
    '''
    Compile bytecode of c source code using CLANG.

    Arguments:
        input_file_path {str} -- Path of c source code file
        output_file_path {str} -- Path to source bytecode file
    '''
    cmd = KLEE_CMD['compile_to_bytecode'].format(
        input=input_file_path,
        output=output_file_path)
    os.system(CMD['bash'].format(cmd))


def symbolic_execution(
        output_path,
        stdin,
        file_name,
        bytecode_file_path,
        options):
    '''
    Perform symbolic execution on bytecode file using Klee.

    Arguments:
        output_path {str} -- Path to store Klee statistics
        stdin {dict} -- Symbolic execution arguments and inputs size
        file_name {str} -- Name of source file
        bytecode_file_path {str} -- Path of bytecode file
        options {dict} -- Memory, timeout options for symbolic exection tool
    '''
    output_dir = os.path.join(output_path, file_name)

    sym_args = ''
    if stdin['num-arg'] >= 1:
        sym_args = KLEE_CMD['sym-args'].format(
            max=str(stdin['num-arg']), length=str(stdin['length-arg']))

    sym_stdin = ''
    if stdin['num-input'] >= 1:
        sym_stdin = KLEE_CMD['sym-stdin'].format(
            length=str(stdin['length-input']))

    cmd = KLEE_CMD['options'].format(
        input=bytecode_file_path,
        output=output_dir,
        memory=str(
            options['memory']),
        time=str(
            options['timeout']),
        search=options['search'],
        sym_args=sym_args,
        sym_stdin=sym_stdin)
    os.system(CMD['bash'].format(cmd))


def time_taken(input_path):
    '''
    Extract time required to run symbolic execution by Klee.

    Arguments:
        input_path {str} -- Path of Klee time statistics file

    Returns:
        float -- Time required to run symbolic exectuion on a bytecode file
                 by Klee
    '''
    time = 0
    cmd = KLEE_CMD['stats'].format(input=input_path)
    content = str(os.popen(cmd).read())

    seconds = re.search(KLEE_RE['kstats-time'], str(content))
    if seconds:
        time = float(seconds.group(0).strip())

    return time


def stats(output_dir_path, credentials):
    '''
    Extract activation codes and passwords from Klee stats file.

    Arguments:
        output_dir_path {str} -- Directory path where Klee stats are saved
        credentials {dict} -- Activation codes and passwords of c program
                              authenticate function

    Returns:
        dict -- Symbolic execution statistics
    '''
    input_ktest_files_path = fs.ls(output_dir_path, EXT['ktest'])

    codes = []
    passwords = []
    for input_ktest_file_path in input_ktest_files_path:
        cmd = KLEE_CMD['ktest'].format(input=input_ktest_file_path)
        content = str(os.popen(cmd).read())

        input_ktest_file = fs.details(input_ktest_file_path)
        output_ktest_file = FILE_NAME['klee-test'].format(
            name=input_ktest_file['name'])
        output_ktest_file_path = os.path.join(
            output_dir_path, output_ktest_file)
        fs.write(output_ktest_file_path, content)

        results = re.findall(KLEE_RE['ktest-text'], content)
        texts = [text.replace('text: ', '').replace('\n', '')
                 for text in results]
        codes = codes + texts
        passwords = passwords + texts

    return {
        'time-taken': time_taken(output_dir_path),
        'generated-codes': lists.to_str_with_nl(codes),
        'generated-passwords': lists.to_str_with_nl(passwords),
        'is-code-cracked': lists.has_string(credentials['codes'], codes),
        'is-password-cracked': lists.has_string(credentials['passwords'], passwords),
    }


def run(input_file_path, output_dir_path, stdin, options, credentials):
    '''
    Run symbolic execution on a c program using Angr.

    Returns:
    Arguments:
        input_file_path {str} -- Input path of compiled c program
        output_dir_path {str} -- Output path to store rest result
        stdin {dict} -- Symbolic execution arguments and inputs size
        options {dict} -- Memory, timeout options for symbolic exection tool
        credentials {dict} -- Activation codes and passwords of c program
                              authenticate function

    Returns:
        dict -- Symbolic execution statistics
    '''
    input_file = fs.details(input_file_path)
    bytecode_file = FILE_NAME['bytecode'].format(name=input_file['name'])
    bytecode_file_path = os.path.join(output_dir_path, bytecode_file)

    compile_to_bytecode(input_file_path, bytecode_file_path)
    symbolic_execution(
        output_dir_path,
        stdin,
        input_file['name'],
        bytecode_file_path,
        options)

    return stats(output_dir_path, credentials)
