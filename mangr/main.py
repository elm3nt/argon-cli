import os
import angr
import claripy

from core.const import *
from utils import file


def symbolic_execution(input_file_path, output_dir_path, stdin):
    project = angr.Project(input_file_path)

    args = []
    if stdin['num-arg'] >= 1:
        for i in range(0, stdin['num-arg']):
            args.append(claripy.BVS('arg'+str(i), int(stdin['arg-length']) * 8))

        entry_state = [input_file_path] + args
        state = project.factory.entry_state(args = entry_state)
    else:
        state = project.factory.entry_state()

    simulation_manager = project.factory.simulation_manager(state)
    simulation_manager.run()

    if hasattr(simulation_manager, 'deadended'):
        for deadended in simulation_manager.deadended:
            for arg in args:
                argv = deadended.solver.eval(arg, cast_to = bytes)
                print('arg: ', argv)

            if stdin['num-input'] >= 1:
                print('input: ', deadended.posix.dumps(0))
                print('input: ', deadended.posix.dumps(1))
                print('input: ', deadended.posix.dumps(2))
                print()


def compile(input_path, output_path):
    gcc = CMD['gcc'].format(input = input_path, output = output_path)
    cmd = CMD['bash'].format(gcc)
    os.system(cmd)

def run(input_file_path, output_dir_path, stdin):
    input_file = file.details(input_file_path)
    output_file_path = os.path.join(output_dir_path, input_file['name'])
    compile(input_file_path, output_file_path)

    symbolic_execution(output_file_path, output_dir_path, stdin)
