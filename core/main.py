import os

from tigress.main import task

def run(argv):
    obfuscation_combinations = {'A', 'ADC'}
    input_path = os.path.abspath(argv[1])
    output_path = os.path.abspath(argv[2])
    no_of_variants = int(argv[3])

    task(input_path, output_path, obfuscation_combinations, no_of_variants)
