
import itertools

from csp import backtracking_search, min_conflicts, mrv, AC3, forward_checking, mac, CSP
import kenken_problems

# var format is '<func>|<result>|<x1,y1>|<x2,y2>|...|<xN,yN>'

def mult(iter):
    res = 1
    for x in iter:
        res *= x

    return res

def varstring_to_xy(varstring):
    for cell in varstring.split('|')[2:]:
        c = cell.split(',')
        yield (int(c[0]), int(c[1]))


def legal(var, values, N):
    # check if vars can have values of values
    rowvals = [[] for x in range(N)]
    colvals = [[] for x in range(N)]

    for (x, y), value in zip(varstring_to_xy(var), values):
        if value in rowvals[x] or value in colvals[y]:
            return False

        rowvals[x].append(value)
        colvals[y].append(value)

    return True

class Kenken(CSP):
    def __init__(self, problem):
        self.problem = problem
        N = self.problem['N']

        # vars that have cells in row[i]
        inrow = [[] for x in range(N)]
        incol = [[] for x in range(N)]

        # vars
        self.variables = problem['sextes']
        self.domains = {}
        for v in self.variables:
            parts = v.split('|')
            func = parts[0]
            target = int(parts[1])
            n_elements = len(parts) - 2 # without func and result

            if func in '-/' and (n_elements != 2 or target < 0 or target > N):
                raise ValueError("come on man")

            # domains -- only the ones that give correct target result
            # a domain is a tuple -> (value of x1y1, value of x2y2, ..., value of xNyN)
            all_domains = list(itertools.product(range(1, N+1), repeat=n_elements))
            if func == '+':
                self.domains[v] = [d for d in all_domains if legal(v, d, N) and sum(d) == target]
            elif func == '*':
                self.domains[v] = [d for d in all_domains if legal(v, d, N) and mult(d) == target]
            elif func == '-':
                self.domains[v] = [d for d in all_domains if legal(v, d, N) and abs(d[0] - d[1]) == target]
            elif func == '/':
                self.domains[v] = [d for d in all_domains if legal(v, d, N) and ((d[0] / d[1] == target) or (d[1] / d[0] == target))]

            # rows and columns of this sexta, used for neighbors below
            for x, y in varstring_to_xy(v):
                inrow[x].append(v)
                incol[y].append(v)

        # neighbors -- only the ones are the ones with elements in the same row
        self.neighbors = {}
        for v in self.variables:
            neighbors = set()

            for x, y in varstring_to_xy(v):
                for n in inrow[x]:
                    neighbors.add(n)

                for n in incol[y]:
                    neighbors.add(n)

            neighbors.remove(v)
            self.neighbors[v] = list(neighbors)

        # print('Variables:', self.variables)
        # print('Domains:', self.domains)
        # print('Neighbors:', self.neighbors)

        CSP.__init__(self, self.variables, self.domains, self.neighbors, self.constraints_func)

    def constraints_func(self, A, value_a, B, value_b):
        vars_A = A.split('|')[2:]
        vars_B = B.split('|')[2:]

        # create a single var for them all
        allvars = 'x|x|' + '|'.join(vars_A + vars_B)
        allvals = (*value_a,*value_b)

        return legal(allvars, allvals, self.problem['N'])

    def display(self, assignment):
        N = self.problem['N']

        grid = [[0 for _ in range(N)] for __ in range(N)]   # NxN zeros
        for var, values in assignment.items():
            for (x, y), val in zip(varstring_to_xy(var), values):
                grid[x][y] = val

        for x in range(N):
            for y in range(N):
                print(grid[x][y], end=' ')
            print()
        
        print('\nNeeded', self.nassigns,'assigns')


if __name__ == '__main__':
    k = Kenken(getattr(kenken_problems, 'six'))

    # print(kenken_problems.__dict__.keys())
    AC3(k)
    k.display(min_conflicts(k))
