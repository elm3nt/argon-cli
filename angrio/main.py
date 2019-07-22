import os
import angr
import claripy
from datetime import datetime

from utils import fs
from utils import lists
from core.const import *
from code.main import compile_code


def init_project(input_file_path, stdin, project):
    args = []
    state = project.factory.entry_state()

    if stdin['num-arg'] >= 1:
        for i in range(0, stdin['num-arg']):
            args.append(claripy.BVS('arg'+str(i), int(stdin['length-arg']) * ONE_BYTE))

        entry_state = [input_file_path] + args
        state = project.factory.entry_state(args = entry_state)

    return {
        'args': args,
        'state': state,
    }


def decode_credentials(output_dir_path, stdin, args, simulation_manager, credentials):
    codes = []
    passwords = []

    test_file_name = FILE_NAME['angr-test'].format(index = '1')
    for deadended in simulation_manager.deadended:
        content = ''
        output_test_file_path = os.path.join(output_dir_path, test_file_name)

        content += 'Arg(s)\n'
        for arg in args:
            code = str(deadended.solver.eval(arg, cast_to = bytes))
            codes.append(code)
        content += lists.to_str_with_nl(codes) + '\n'

        content += '\nInput(s)\n'
        if stdin['num-input'] >= 1:
            dump_0 = str(deadended.posix.dumps(0))
            print('input: ', dump_0)
            passwords.append(dump_0)
            dump_1 = str(deadended.posix.dumps(1))
            print('input: ', dump_1)
            passwords.append(dump_1)
            dump_2 = str(deadended.posix.dumps(2))
            print('input: ', dump_2)
            passwords.append(dump_2)
            print()
        content += lists.to_str_with_nl(passwords) + '\n'

    fs.write(output_test_file_path, content)

    return {
        'codes': codes,
        'passwords': passwords,
    }


def symbolic_execution(input_file_path, output_dir_path, stdin, options, credentials):
    start_time = datetime.now()

    project = angr.Project(input_file_path)
    project_status = init_project(input_file_path, stdin, project)
    simulation_manager = project.factory.simulation_manager(project_status['state'])
    simulation_manager.run()

    end_time = datetime.now()
    time_taken = end_time - start_time

    generated = {
        'codes': [],
        'passwords': [],
    }
    if hasattr(simulation_manager, 'deadended'):
        generated = decode_credentials(output_dir_path, stdin, project_status['args'], simulation_manager, credentials)

    return {
        'time-taken': time_taken.total_seconds(),
        'generated-codes': lists.to_str_with_nl(generated['codes']),
        'generated-passwords': lists.to_str_with_nl(generated['passwords']),
        'is-code-cracked': lists.has_string(credentials['codes'], generated['codes']),
        'is-password-cracked': lists.has_string(credentials['passwords'], generated['passwords']),
    }


def run(input_file_path, output_dir_path, stdin, options, credentials):
    compiled_code_path = compile_code(input_file_path, output_dir_path)

    return symbolic_execution(compiled_code_path, output_dir_path, stdin, options, credentials)
