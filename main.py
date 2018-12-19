from kenken import KENKEN
from csp import *
import problems.ekfwnhsh, problems.hard, problems.veryhard


problem = problems.veryhard.problem
puzzle = KENKEN(problem)

#####################################################

### AC3 (optional)
AC3(puzzle)

### BT
ass = backtracking_search(puzzle)

### BT_MRV
# ass = backtracking_search(puzzle, mrv)

# ### FC
# ass = backtracking_search(puzzle, inference=forward_checking)

# ### FC_MRV
# ass = backtracking_search(puzzle, mrv, inference=forward_checking)

# ### MAC
# ass = backtracking_search(puzzle, inference=mac)

#####################################################


if ass is None:
    print('rip')
else:
    puzzle.print(ass)