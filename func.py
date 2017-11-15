import random
import os


FOLLOW_UP_TESTS = 'follow-up-tests'


def transform(clauses):
    # List of 50 transformations
    result = []

    for i in range(0, 50):
        copy = list(clauses)
        random.shuffle(copy)

        result.append(copy)

    return result


def do_func(sut_path, inputs_path, seed):
    if seed is not None:
        random.seed(seed)
    else:
        random.seed()

        # TODO: implement do_func

    for x in range(1, 21):
        with open(os.path.join(inputs_path, str(x).zfill(2) + '.cnf')) as formula:
            first_line = formula.readline()

            p, cnf, no_of_vars, no_of_clauses = first_line.strip().split()

            clauses = []

            for line in formula:
                clauses.append(line.split())

        new_formulae = transform(clauses)

        if not os.path.exists(FOLLOW_UP_TESTS):
            os.makedirs(FOLLOW_UP_TESTS)

        for i, new_formula in enumerate(new_formulae):
            print('Formula {}: Writing transformation {}'.format(x, i))

            cnf_filename = os.path.join(FOLLOW_UP_TESTS, '{}_{}.cnf'.format(str(x).zfill(2), str(i).zfill(2)))
            txt_filename = os.path.join(FOLLOW_UP_TESTS, '{}_{}.txt'.format(str(x).zfill(2), str(i).zfill(2)))

            with open(cnf_filename, 'w') as new_cnf, open(txt_filename, 'w') as new_txt:
                # TODO: You might change some values
                new_cnf.write(first_line)

                for line in new_formula:
                    new_line = ' '.join(map(lambda lit: str(lit), line)) + '\n'
                    new_cnf.write(new_line)

                new_txt.write('SAT->SAT\n')
                new_txt.write('UNSAT->UNSAT\n')
