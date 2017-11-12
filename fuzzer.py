import sys

import func
import ub

if __name__ == '__main__':
    sut_path = None
    inputs_path = None
    mode = None

    try:
        sut_path = sys.argv[1]
        inputs_path = sys.argv[2]
        mode = sys.argv[3]
    except IndexError:
        print('Provide at least 3 parameters')
        exit(1)

    if len(sys.argv) == 5:
        seed = sys.argv[4]
    else:
        seed = None

    # TODO: check parameters correctness

    if mode == 'ub':
        ub.do_ub(sut_path, inputs_path, seed)
    elif mode == 'func':
        func.do_func(sut_path, inputs_path, seed)
    else:
        print('The mode parameter must be either ub or func')
