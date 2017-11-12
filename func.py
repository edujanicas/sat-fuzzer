import random


def do_func(sut_path, inputs_path, seed):
    if seed is not None:
        random.seed(seed)
    else:
        random.seed()

        # TODO: implement do_func
