import os

from tigress.main import task, generate

def run(argv):
    if argv[1] == 'generate':
        input_path = os.path.abspath(argv[2])
        output_path = os.path.abspath(argv[3])
        password = argv[4]
        pin = argv[5]

        generate(input_path, output_path, password, pin)

    elif argv[1] == 'obfuscate':
        obfuscation_combinations = {'A', 'ADC'}
        input_path = os.path.abspath(argv[2])
        output_path = os.path.abspath(argv[3])
        no_of_variants = int(argv[4])

        task(input_path, output_path, obfuscation_combinations, no_of_variants)
