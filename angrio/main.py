import os
import angr
import claripy
from datetime import datetime

from utils import file
from utils import lists
from core.const import *


def symbolic_execution(input_file_path, output_dir_path, stdin, options, credentials):
    start_time = datetime.now()

    project = angr.Project(input_file_path)

    args = []
    if stdin['num-arg'] >= 1:
        for i in range(0, stdin['num-arg']):
            args.append(claripy.BVS('arg'+str(i), int(stdin['length-arg']) * ONE_BYTE))

        entry_state = [input_file_path] + args
        state = project.factory.entry_state(args = entry_state)
    else:
        state = project.factory.entry_state()

    simulation_manager = project.factory.simulation_manager(state)
    simulation_manager.run()

    end_time = datetime.now()

    if hasattr(simulation_manager, 'deadended'):
        index = 0

        codes = ''
        passwords = ''
        generated_codes = []
        generated_passwords = []

        for deadended in simulation_manager.deadended:
            content = ''
            test_file_name = FILE_NAME['angr-test'].format(index = str(index))
            output_test_file_path = os.path.join(output_dir_path, test_file_name)

            content += 'Arg(s)\n'
            for arg in args:
                code = str(deadended.solver.eval(arg, cast_to = bytes))
                print('arg: ', code)
                generated_codes.append(code)
            content += '\n'.join(generated_codes) + '\n'

            content += '\nInput(s)\n'
            if stdin['num-input'] >= 1:
                dump_0 = str(deadended.posix.dumps(0))
                print('input: ', dump_0)
                generated_passwords.append(dump_0)
                dump_1 = str(deadended.posix.dumps(1))
                print('input: ', dump_1)
                generated_passwords.append(dump_1)
                dump_2 = str(deadended.posix.dumps(2))
                print('input: ', dump_2)
                generated_passwords.append(dump_2)
                print()
            content += '\n'.join(generated_passwords) + '\n'

            with open(output_test_file_path, 'w') as test_file:
                test_file.write(content)

            index += 1

    time_taken = end_time - start_time

    return {
        'generated-codes': generated_codes,
        'time-taken': time_taken.total_seconds(),
        'generated-passwords': generated_passwords,
        'is-code-cracked': lists.has_string(credentials['code'], generated_codes),
        'is-password-cracked': lists.has_string(credentials['password'], generated_passwords),
    }


def compile(input_path, output_path):
    gcc = CMD['gcc'].format(input = input_path, output = output_path)
    cmd = CMD['bash'].format(gcc)
    os.system(cmd)


def run(input_file_path, output_dir_path, stdin, options, credentials):
    input_file = file.details(input_file_path)
    output_file = FILE_NAME['c-out'].format(name = input_file['name'])
    output_file_path = os.path.join(output_dir_path, output_file)
    compile(input_file_path, output_file_path)

    return symbolic_execution(output_file_path, output_dir_path, stdin, options, credentials)
