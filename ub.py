import random
import subprocess

import util

SAVED_INPUTS_PATH = "fuzzed-tests/"
saved_inputs_id = 0


def do_ub(sut_path, inputs_path, seed):
    if seed is not None:
        random.seed(seed)
    else:
        random.seed()

    while True:
        input_text = create_input()

        # TODO: timeout
        ub = run_sut(input_text, sut_path)

        if ub is not None:
            save_input(input_text)


def create_input():
    return "p cnf 0 0"


def run_sut(input_text, sut_path):
    subprocess.Popen([sut_path, input_text])
    # TODO check for undefined behaviour
    return True


def save_input(input_text):
    global saved_inputs_id

    # TODO decide what to do after 20 inputs have been found
    util.save_text(SAVED_INPUTS_PATH + "interesting_input{}.txt".format(saved_inputs_id), input_text)

    saved_inputs_id = (saved_inputs_id + 1) % 20
