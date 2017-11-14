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
    "SIGNED_INTEGER_OVERFLOW_REGEX": re.compile('^runtime.+signed integer')
}


def do_ub(sut_path, inputs_path, seed):
    if seed is not None:
        random.seed(seed)
    else:
        random.seed()

    i = 0

    while True:
        if i == 0:
            print("Sending input")
            input_file = create_input()
        elif i == 1:
            print("Sending garbage")
            input_file = create_garbage()

        sut_output = run_sut(input_file, sut_path)

        if sut_output is not None:
            ubs = check_ub(sut_output)

            if ubs > 0:
                save_input(input_file)

        input_file.close()

        i += 1
        i = i % 2


def create_input():
    number_of_formulas = 100000
    number_of_literals = 1000
    formulas_width = 10

    cnf = "p cnf " + str(number_of_literals) + " " + str(number_of_formulas) + "\n"

    for i in range(0, number_of_formulas):
        for j in range(0, formulas_width):
            cnf += random.choice(["", "-"])
            cnf += str(1 + int(random.random() * (number_of_literals - 1))) + " "
        cnf += "0\n"

    return make_cnf_file(cnf)


def create_garbage():
    cnf = "p cnf 10 20\n"
    choice = 0

    while True:
        if choice == 0:
            if len(cnf) >= 20:
                break
        elif choice == 1:
            cnf += string.punctuation
        elif choice == 2:
            cnf += string.printable
        elif choice == 3:
            cnf += string.digits
        elif choice == 4:
            cnf += '0'
        elif choice == 5:
            cnf += '\n'

        choice = random.randint(0, 5)

    return make_cnf_file(cnf)


def make_cnf_file(cnf):
    input_file = tempfile.NamedTemporaryFile(mode='w')
    input_file.write(cnf)
    input_file.flush()
    return input_file


def run_sut(input_file, sut_path):
    result = subprocess.Popen(["./runsat.sh", input_file.name], stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                              cwd=sut_path)

    try:
        sut_output, sut_error = result.communicate()
        sut_output_printable = sut_output.decode('ascii').split('\n')
        for line in sut_output_printable:
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
