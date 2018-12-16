# kenken.py
# Solve Kenken as a CSP problem

import csp


####################################################

'''
sextes should be dictionaries
{
    vars: [list of vars participating],
    func: one of '+*/-'
    target: int
}
'''

# simple example
SIMPLE_SEXTES = [{
    'vars': [0,1],
    'func': '*',
    'target': 2
}, {
    'vars': [2, 3],
    'func': '-',
    'target': 1
}]

# simple 2
SIMPLE2_SEXTES = [{
    'vars': [0, 1, 2, 3, 4, 5],
    'func': '*',
    'target': 36
}, {
    'vars': [6, 7, 8],
    'func': '+',
    'target': 6
}]

def _(x, y):
    return x * 6 + y

# ekfwnhsh
EKFWNHSH_SEXTES = [{
    'vars': [_(0, 0), _(1, 0)],
    'func': '+',
    'target': 11
}, {
    'vars': [_(0, 1), _(0, 2)],
    'func': '/',
    'target': 2
}, {
    'vars': [_(1, 1), _(1, 2)],
    'func': '-',
    'target': 3
}, {
    'vars': [_(0, 3), _(1, 3)],
    'func': '*',
    'target': 20
}, {
    'vars': [_(0, 4), _(0, 5), _(1, 5), _(2, 5)],
    'func': '*',
    'target': 6
}, {
    'vars': [_(1, 4), _(2, 4)],
    'func': '/',
    'target': 3
}, {
    'vars': [_(2, 2), _(2, 3)],
    'func': '*',
    'target': 6
}, {
    'vars': [_(2, 0), _(2, 1), _(3, 0), _(3, 1)],
    'func': '*',
    'target': 240
}, {
    'vars': [_(4, 0), _(4, 1)],
    'func': '*',
    'target': 6
}, {
    'vars': [_(3, 2), _(4, 2)],
    'func': '*',
    'target': 6
}, {
    'vars': [_(3, 3), _(4, 3), _(4, 4)],
    'func': '+',
    'target': 7
}, {
    'vars': [_(3, 4), _(3, 5)],
    'func': '*',
    'target': 30
}, {
    'vars': [_(5, 0), _(5, 1), _(5, 2)],
    'func': '+',
    'target': 8
}, {
    'vars': [_(5, 3), _(5, 4)],
    'func': '/',
    'target': 2
}, {
    'vars': [_(4, 5), _(5, 5)],
    'func': '+',
    'target': 9
}]

################################################################


# util

def find_sexta(var, sextes):
    for c in sextes:
        if var in c['vars']:
            return c

    raise Exception("all vars must be in a sexta")

####################################################################

class KenKen(csp.CSP):
    '''
    @N: grid size
    @sextes: list of click dictionaries
    '''
    def __init__(self, N, sextes):
        self.N = N
        self.sextes = sextes
        self.variables = []
        self.domains = {}
        self.neighbors = {}

        # speeds up constraints()
        self.sexta_of = {}

        # sanity check sextes
        for sexta in sextes:
            if sexta['func'] not in '+-*/':
                raise ValueError("unknown sexta func")

            if sexta['target'] < 0:
                raise ValueError("bad target value")

            if sexta['func'] in '/-' and len(sexta['vars']) != 2:
                raise ValueError("- and / need exactly two sextmates")

        RN = range(N)
        DOMAIN = [x+1 for x in range(N)]

        # variables, domains, and neighbors
        for x in RN:
            for y in RN:
                var = x * N + y

                # add var and domain
                self.variables.append(var)
                self.domains[var] = list(DOMAIN)

                # find sextmates
                sexta = find_sexta(var, sextes)
                sextmates = list(sexta['vars'])
                sextmates.remove(var)
                self.sexta_of[var] = {
                    'vars': sextmates,
                    'func': sexta['func'],
                    'target': sexta['target']
                }

                # neighbors
                same_row_neighbors = [(x * N + i) for i in RN if i != y]
                same_col_neighbors = [(i * N + y) for i in RN if i != x]
                sext_neighbors = sextmates

                # list -> set -> list, to get rid of duplicates
                self.neighbors[var] = list(set(same_col_neighbors + same_row_neighbors + sext_neighbors))

        csp.CSP.__init__(self, self.variables, self.domains, self.neighbors, self.constraints_func)

    def constraints_func(self, A, value_a, B, value_b):
        N = self.N
        asss = self.infer_assignment()
        # print(f'Checking {A}={value_a}\t and {B}={value_b}\t, \t{len(asss)} assngs = {asss}')

        # cant have a value twice on the same row or col
        A_x, A_y = A // N, A % N
        B_x, B_y = B // N, B % N
        if (A_x == B_x or A_y == B_y) and value_a == value_b:
            # print('no')
            return False

        # more checks for sextmates
        sexta_of_B = self.sexta_of[B]
        func, target = sexta_of_B['func'], sexta_of_B['target']
        if A in sexta_of_B['vars'] and func in '-/':
                maxval = max(value_a, value_b)
                minval = min(value_a, value_b)

                if func == '-':
                    return maxval - minval == target
                elif func == '/':
                    return maxval / minval == target
        elif A in sexta_of_B['vars'] and func in '+*':
            min_sexta_values = {k: min(self.curr_domains[k]) for k in sexta_of_B['vars'] if k != A}
            min_sexta_values[A] = value_a

            res = value_b
            for var in min_sexta_values:
                res = (res + min_sexta_values[var]) if func == '+' else (res * min_sexta_values[var])

            cnt = 0
            for var in sexta_of_B['vars']:
                if var == A:
                    continue

                if len(self.curr_domains[var]) == 1:
                    cnt += 1

            if cnt == len(sexta_of_B['vars']) - 1:
                return res == target                  # all assigned
            else:
                return res <= target                   # some remain to be assigned

        return True

    def display(self, assignment):
        for i in range(self.N):
            for j in range(self.N):
                print(assignment[i*self.N + j], end=' ')
            print()



#################################################################

from datetime import datetime

import timeit

if __name__ == '__main__':
    k = KenKen(6, EKFWNHSH_SEXTES)

    # for x in k.variables:
    #     print(x, k.sexta_of[x])

    t = datetime.now()
    k.display(csp.backtracking_search(k, select_unassigned_variable=csp.mrv))
    t2 = datetime.now()

    print(t2 - t, 'seconds')
