
import itertools
import csp

# variables are
#
# '(x_1*N + y_1)_(x_2*N + y_2)_(...)_(x_N * N + y_N)'

#####################################################################

class KENKEN(csp.CSP):
    def __init__(self, puzzle):
        self.size = puzzle['size']

        N = self.size

        self.vars_with_row = {}
        self.vars_with_col = {}

        self.variables = []
        self.domains = {}
        for eachvar in puzzle['vars']:
            varname = eachvar['cells']
            cells = self.list_of_cells(varname)
            res = eachvar['result']
            action = eachvar['action']
            all_to_try = list(itertools.product(range(1, N+1), repeat=len(cells)))

            self.variables.append(varname)
            self.domains[varname] = []

            if action == 'sum':
                self.domains[varname] = list(filter(lambda d : self.possible(varname, d, N) and sum(d) == res, all_to_try))
            elif action == 'mul':
                self.domains[varname] = list(filter(lambda d : self.possible(varname, d, N) and self.product_of_all(d) == res, all_to_try))
            elif action == 'div':
                self.domains[varname] = list(filter(lambda d : self.possible(varname, d, N) and max(d) / min(d) == res, all_to_try))
            elif action == 'sub':
                self.domains[varname] = list(filter(lambda d : self.possible(varname, d, N) and max(d) - min(d) == res, all_to_try))

            for cell in cells:
                row, col = self.cell_to_xy(cell, N)

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

        self.neighbors = {}
        for var in puzzle['vars']:
            varname = var['cells']

            neighbors = set()

            for cell in self.list_of_cells(varname):
                row, col = self.cell_to_xy(cell, N)

                for x in self.vars_with_col[col]:
                    neighbors.add(x)

                for y in self.vars_with_row[row]:
                    neighbors.add(y)

            try:
                neighbors.remove(varname)
            except:
                pass

            self.neighbors[varname] = list(neighbors)

        super().__init__(self.variables, self.domains, self.neighbors, self.checkok)

    def print(self, ass):
        N = self.size

        grid = {}

        for var in ass:
            values = ass[var]
            for cell, value in zip(self.list_of_cells(var), values):
                row, col = self.cell_to_xy(cell, N)

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

        return self.possible(all_cells, all_values, self.size)

    def product_of_all(self, l):
        p = 1
        for x in l:
            p *= x

        return p

    def list_of_cells(self, var):
        return var.split('_')

    def cell_to_xy(self, cell, N):
        return (int(cell) // N), (int(cell) % N)

    def possible(self, variable, values, N):
        # rows[x] will contain the values from row @x
        rows = { }
        # cols[y] will contain the values from column @y
        cols = { }

        for cell, val in zip(self.list_of_cells(variable), values):
            row, col = self.cell_to_xy(cell, N)

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