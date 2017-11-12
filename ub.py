import os.path
import random
import subprocess
import tempfile

import util

SAVED_INPUTS_PATH = "fuzzed-tests/"
saved_inputs_id = 0


def do_ub(sut_path, inputs_path, seed):
    if seed is not None:
        random.seed(seed)
    else:
        random.seed()

    while True:
        input_file = create_input()

        # TODO: timeout
        ub = run_sut(input_file, sut_path)

        if ub is not None:
            save_input(input_file)


def create_input():
    cnf = "p cnf 0 0"
    input_file = tempfile.NamedTemporaryFile(mode='w')
    input_file.write(cnf)
    return input_file


def run_sut(input_file, sut_path):
    result = subprocess.run([os.path.join(sut_path, "runsat.sh"), input_file.name], stderr=subprocess.PIPE)
    run_output = result.stderr.decode('ascii').split('\n')[:-1]
    # TODO check for undefined behaviour
    return True


def save_input(input_file):
    global saved_inputs_id

    # TODO decide what to do after 20 inputs have been found
    util.save_text(SAVED_INPUTS_PATH + "interesting_input{}.txt".format(saved_inputs_id), input_file.name)

    saved_inputs_id = (saved_inputs_id + 1) % 20
