# test.py
# Run kenken many times and get results

import kenken, kenken_problems
import csp
import time

#############################################################################

def BT(p):
    csp.backtracking_search(p)

def BT_MRV(p):
    # csp.AC3(p)
    csp.backtracking_search(p, csp.mrv)

def FC(p):
    csp.backtracking_search(p, inference=csp.forward_checking)

def FC_MRV(p):
    # csp.AC3(p)
    csp.backtracking_search(p, csp.mrv, inference=csp.forward_checking)

def MAC(p):
    # csp.AC3(p)
    csp.backtracking_search(p, inference=csp.mac)

#############################################################################

def run_test(solver, problem):
    c = kenken.Kenken(problem)

    start = time.clock()
    # csp.AC3(c)
    solver(c)
    end = time.clock()

    # print('Time:\t\t', end-start,'seconds')
    # print('N Assigns:\t',c.nassigns)

    return end-start, c.nassigns


def run_ntimes(solver, problem, n):
    print('--------')
    print(str(solver), str(problem['N']))
    mean_time = 0
    mean_nassigns = 0
    for _ in range(n):
        time, nassigns = run_test(solver, problem)

        mean_time += time
        mean_nassigns += nassigns

    mean_time /= n
    mean_nassigns //= n

    print('Average Time:\t\t', mean_time, 'seconds')
    print('Average Assigns:\t', mean_nassigns)

#############################################################################

# for s in BT, BT_MRV, FC, FC_MRV, MAC:
for s in [BT, BT_MRV, FC, FC_MRV, MAC]:
    for problem in kenken_problems.all:
        run_ntimes(s, problem, 10)