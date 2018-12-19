from kenken import KENKEN
from csp import *
import problems.ekfwnhsh, problems.hard, problems.veryhard


problem = problems.veryhard.problem
puzzle = KENKEN(problem)

#####################################################

### AC3 (optional)
# AC3(puzzle)

ass = backtracking_search(puzzle) ### BT
# ass = backtracking_search(puzzle, select_unassigned_variable=mrv) ### BT_MRV
# ass = backtracking_search(puzzle, inference=forward_checking) ### FC
# ass = backtracking_search(puzzle, select_unassigned_variable=mrv, inference=forward_checking) ### FC_MRV
# ass = backtracking_search(puzzle, inference=mac) ### MAC

#####################################################


if ass is None:
    print('rip')
else:
    puzzle.print(ass)
    # print(puzzle.nassigns)