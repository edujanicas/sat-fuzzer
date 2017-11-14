import random
import re
import string
import subprocess
import tempfile

import util

SAVED_INPUTS_PATH = "fuzzed-tests/"
saved_inputs_id = 0

REGEXES = {
    "INTMIN_NEGATED_REGEX": re.compile('^runtime.+negation'),
    "NULLPOINTER_REGEX": re.compile('^runtime.+null pointer'),
    "SHIFT_ERROR_REGEX": re.compile('^runtime.+shift'),
    "USE_AFTER_FREE_REGEX": re.compile('^==.*AddressSanitizer: heap-use-after-free'),
    "HEAP_BUFFER_OVERFLOW_REGEX": re.compile('^==.*AddressSanitizer: heap-buffer-overflow'),
    "STACK_BUFFER_OVERFLOW_REGEX": re.compile('^==.*AddressSanitizer: stack-buffer-overflow'),
    "SIGNED_INTEGER_OVERFLOW_REGEX": re.compile('^runtime.+signed integer')}


def do_ub(sut_path, inputs_path, seed):
    if seed is not None:
        random.seed(seed)
    else:
        random.seed()

    while True:
        input_file = create_input()

        sut_output = run_sut(input_file, sut_path)

        if sut_output is not None:
            ubs = check_ub(sut_output)

            if ubs > 0:
                save_input(input_file)

        input_file.close()


def create_input():
    cnf = "p cnf 10 100\n"

    for i in range(0, 100):
        for j in range(0, 5):
            cnf += random.choice(string.digits) + " "
        cnf += "0\n"

    input_file = tempfile.NamedTemporaryFile(mode='w')
    input_file.write(cnf)
    input_file.flush()
    return input_file


def run_sut(input_file, sut_path):
    result = subprocess.Popen(["./runsat.sh", input_file.name], stderr=subprocess.PIPE, stdout=subprocess.PIPE,
                              cwd=sut_path)

    try:
        sut_output, sut_error = result.communicate(timeout=5)
        for line in sut_output.decode('ascii'):
            print(line)
        return sut_error

    except subprocess.TimeoutExpired:
        result.kill()
        result.communicate()
        print("TIMED OUT")

    return None


def save_input(input_file):
    global saved_inputs_id

    # TODO decide what to do after 20 inputs have been found
    util.save_text(SAVED_INPUTS_PATH + "interesting_input{}.txt".format(saved_inputs_id), input_file.name)

    saved_inputs_id = (saved_inputs_id + 1) % 20


def check_ub(sut_error):
    ubs = 0
    for line in sut_error.decode('ascii '):
        for key, value in REGEXES.items():
            if value.match(line):
                print(line)
                ubs += 1

    return ubs
