import os
import re
import sys
import shutil

from .const import *
from utils import fs
from utils import lists
from core.const import *
from pathlib import Path


def compile(input_file_path, output_file_path):
    cmd = KLEE_CMD['compile'].format(
        input=input_file_path,
        output=output_file_path)
    os.system(CMD['bash'].format(cmd))


def symbolic_execution(
        output_path,
        stdin,
        file_name,
        bytecode_file_path,
        options):
    output_dir = os.path.join(output_path, file_name)

    sym_args = ''
    if (stdin['num-arg'] >= 1):
        sym_args = KLEE_CMD['sym-args'].format(
            max=str(stdin['num-arg']), length=str(stdin['length-arg']))

    sym_stdin = ''
    if (stdin['num-input'] >= 1):
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
    time = 0
    cmd = KLEE_CMD['stats'].format(input=input_path)
    content = str(os.popen(cmd).read())

    seconds = re.search(KLEE_RE['kstats-time'], str(content))
    if seconds:
        time = float(seconds.group(0).strip())

    return time


def stats(output_dir_path, credentials):
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
    input_file = fs.details(input_file_path)
    bytecode_file = FILE_NAME['bytecode'].format(name=input_file['name'])
    bytecode_file_path = os.path.join(output_dir_path, bytecode_file)

    compile(input_file_path, bytecode_file_path)
    symbolic_execution(
        output_dir_path,
        stdin,
        input_file['name'],
        bytecode_file_path,
        options)

    return stats(output_dir_path, credentials)
