from core.const import *
from stats.const import CSV_HEAD as HEAD


def get_csv_header(tool, credentials = { 'codes': [], 'passwords': [] }):
    left = [ HEAD['file-name'], HEAD['file-size'] ]
    middle = []
    right = [ HEAD['file-path'] ]

    if tool == RUN:
        middle = [ HEAD['optimization-level'], HEAD['run-time'] ]

    elif tool == ANGR:
        middle = [ HEAD['angr-time'] ]

        if len(credentials['codes']):
            middle += [ HEAD['codes'], HEAD['angr-is-code-cracked'], HEAD['angr-generated-codes'] ]

        if len(credentials['passwords']):
            middle += [ HEAD['passwords'], HEAD['angr-is-password-cracked'], HEAD['angr-generated-passwords'] ]

    elif tool == KLEE:
        middle = [ HEAD['klee-time'] ]

        if len(credentials['codes']):
            middle += [ HEAD['codes'], HEAD['klee-is-code-cracked'], HEAD['klee-generated-codes'] ]

        if len(credentials['passwords']):
            middle += [ HEAD['passwords'], HEAD['klee-is-password-cracked'], HEAD['klee-generated-passwords'] ]

    elif tool == ALL:
        middle = [ HEAD['run-time'], HEAD['angr-time'], HEAD['klee-time'] ]

        if len(credentials['codes']):
            middle += [ HEAD['codes'], HEAD['angr-is-code-cracked'], HEAD['angr-generated-codes'],
                        HEAD['klee-is-code-cracked'], HEAD['klee-generated-codes'] ]

        if len(credentials['passwords']):
            middle += [ HEAD['passwords'], HEAD['angr-is-password-cracked'], HEAD['angr-generated-passwords'],
                        HEAD['klee-is-password-cracked'], HEAD['klee-generated-passwords'] ]

    return left + middle + right

