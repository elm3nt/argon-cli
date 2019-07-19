import csv

from core.const import *
from .const import CSV_HEAD as HEAD


def write_to_file(output_file_path, data):
    with open(output_file_path, 'w') as file:
        writer = csv.writer(file)
        writer.writerows(data)


def get_csv_header(tool):
    left = [ HEAD['file-name'], HEAD['file-size'] ]
    middle = []
    right = [ HEAD['file-path'] ]

    if tool == RUN or tool == OBFUSCATE:
        middle = [ HEAD['run-time'] ]

    elif tool == ANGR:
        middle = [ HEAD['angr-time'], HEAD['angr-is-code-cracked'], HEAD['angr-is-password-cracked'],
                   HEAD['angr-generated-codes'], HEAD['angr-generated-passwords'] ]

    elif tool == KLEE:
        middle = [ HEAD['klee-time'], HEAD['klee-is-code-cracked'], HEAD['klee-is-password-cracked'],
                   HEAD['klee-generated-codes'], HEAD['klee-generated-passwords'] ]

    elif tool == ALL:
        middle = [ HEAD['run-time'], HEAD['angr-time'], HEAD['klee-time'], HEAD['angr-is-code-cracked'],
                   HEAD['klee-is-code-cracked'], HEAD['angr-is-password-cracked'], HEAD['klee-is-password-cracked'],
                   HEAD['angr-generated-codes'], HEAD['klee-generated-codes'], HEAD['angr-generated-passwords'],
                   HEAD['klee-generated-passwords'] ]

    return left + middle + right

