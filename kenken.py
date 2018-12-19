
import itertools, csp, kenken_problems

# variables are
#
# '(x1*N + y1)_(x2*N + y2)_(...)_(xN * N + yN)'

def product_of_all(l):
    p = 1
    for x in l:
        p *= x

    return p

def list_of_cells(var):
    return var.split('_')

def cell_to_xy(cell, N):
    return (int(cell) // N), (int(cell) % N)


#####################################################################


def possible(variable, values, N):
    # rows[x] will contain the values from row @x
    rows = { }
    # cols[y] will contain the values from column @y
    cols = { }

    for cell, val in zip(list_of_cells(variable), values):
        row, col = cell_to_xy(cell, N)

        try:
            if val in rows[row]:
                return False
        except KeyError:
            rows[row] = set()
        finally:
            rows[row].add(val)

        try:
            if val in cols[col]:
                return False
        except KeyError:
            cols[col] = set()
        finally:
            cols[col].add(val)

    return True

class Kenken(csp.CSP):
    def __init__(self, puzzle):
        self.size = puzzle['size']

        N = self.size

        self.vars_with_row = {}
        self.vars_with_col = {}

        self.variables = []
        self.domains = {}
        for eachvar in puzzle['vars']:
            varname = eachvar['cells']
            cells = list_of_cells(varname)
            res = eachvar['result']
            action = eachvar['action']
            all_to_try = list(itertools.product(range(1, N+1), repeat=len(cells)))
            
            self.variables.append(varname)
            self.domains[varname] = []

            if action == 'sum':
                self.domains[varname] = [d for d in all_to_try if possible(varname, d, N) and sum(d) == res]
            elif action == 'mul':
                self.domains[varname] = [d for d in all_to_try if possible(varname, d, N) and product_of_all(d) == res]
            elif action == 'div':
                self.domains[varname] = [d for d in all_to_try if possible(varname, d, N) and max(d) / min(d) == res]
            elif action == 'sub':
                self.domains[varname] = [d for d in all_to_try if possible(varname, d, N) and max(d) - min(d) == res]

            for cell in cells:
                row, col = cell_to_xy(cell, N)

                try:
                    self.vars_with_row[row].add(varname)
                except KeyError:
                    self.vars_with_row[row] = set()
                    self.vars_with_row[row].add(varname)

                try:
                    self.vars_with_col[col].add(varname)
                except KeyError:
                    self.vars_with_col[col] = set()
                    self.vars_with_col[col].add(varname)

        # for i, items in self.vars_with_col.items():
            # print(i, items)

        self.neighbors = {}
        for var in puzzle['vars']:
            varname = var['cells']

            neighbors = set()

            for cell in list_of_cells(varname):
                row, col = cell_to_xy(cell, N)

                for x in self.vars_with_col[col]:
                    neighbors.add(x)

                for y in self.vars_with_row[row]:
                    neighbors.add(y)

            try:
                neighbors.remove(varname)
            except:
                pass
            
            self.neighbors[varname] = list(neighbors)
            print(varname, self.neighbors[varname])

        # print('Variables:', self.variables)
        # print('Domains:', self.domains)
        # print('Neighbors:', self.neighbors)

        super().__init__(self.variables, self.domains, self.neighbors, self.checkok)

    def display(self, ass):
        N = self.size

        grid = {}

        for var in ass:
            values = ass[var]
            for cell, value in zip(list_of_cells(var), values):
                row, col = cell_to_xy(cell, N)

                grid[str(row)+'-'+str(col)] = str(value)

        print('-' + '+-' * (N-1))
        for x in range(N):
            print('|'.join([grid[str(x) + '-' + str(y)] for y in range(N)]))
            print('-' + '+-' * (N-1))

    def checkok(self, A, a, B, b):
        # concatanate into a single list, to use the already defined 'possible' method
        all_cells = A + '_' + B
        all_values = []
        for v in a:
            all_values.append(v)
        for v in b:
            all_values.append(v)

        return possible(all_cells, all_values, self.size)

import problems.six, problems.hard, problems.nine

if __name__ == '__main__':
    k = Kenken(problems.nine.problem)

    # print(kenken_problems.__dict__.keys())
    # csp.AC3(k)
    k.display(csp.backtracking_search(k))
