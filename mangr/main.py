import os
import angr
import claripy
from datetime import datetime

from .const import *
from utils import file
from core.const import *


def symbolic_execution(input_file_path, output_dir_path, stdin):
    start_time = datetime.now()

    project = angr.Project(input_file_path)

    args = []
    if stdin['num-arg'] >= 1:
        for i in range(0, stdin['num-arg']):
            args.append(claripy.BVS('arg'+str(i), int(stdin['length-arg']) * 8))

        entry_state = [input_file_path] + args
        state = project.factory.entry_state(args = entry_state)
    else:
        state = project.factory.entry_state()

    simulation_manager = project.factory.simulation_manager(state)
    simulation_manager.run()

    end_time = datetime.now()

    if hasattr(simulation_manager, 'deadended'):
        index = 0

        for deadended in simulation_manager.deadended:
            content = ''
            test_file_name = FILE_NAME['test'].format(index = str(index))
            output_test_file_path = os.path.join(output_dir_path, test_file_name)

            content += 'Arg(s)\n'
            for arg in args:
                argv = deadended.solver.eval(arg, cast_to = bytes)
                content += str(argv) + '\n'
                print('arg: ', argv)

            content += '\nInput(s)\n'
            if stdin['num-input'] >= 1:
                content += str(deadended.posix.dumps(0)) + '\n'
                content += str(deadended.posix.dumps(1)) + '\n'
                content += str(deadended.posix.dumps(2)) + '\n'
                print('input: ', deadended.posix.dumps(0))
                print('input: ', deadended.posix.dumps(1))
                print('input: ', deadended.posix.dumps(2))
                print()

            with open(output_test_file_path, 'w') as test_file:
                test_file.write(content)

            index += 1

    time_taken = end_time - start_time

    return {
        'time': time_taken.total_seconds()
    }

def compile(input_path, output_path):
    gcc = CMD['gcc'].format(input = input_path, output = output_path)
    cmd = CMD['bash'].format(gcc)
    os.system(cmd)

def run(input_file_path, output_dir_path, stdin):
    input_file = file.details(input_file_path)
    output_file_path = os.path.join(output_dir_path, input_file['name'])
    compile(input_file_path, output_file_path)

    test_details = symbolic_execution(output_file_path, output_dir_path, stdin)

    return test_details
