
import kenken, kenken_problems, csp
import time


# run minconflicts for all
for x in kenken_problems.all:
    print('Running for N=',x['N'])

    # setup
    k = kenken.Kenken(x)

    # AC3 to reduce domains
    csp.AC3(k)

    start = time.clock()
    sol = csp.min_conflicts(k)
    end = time.clock()
    if sol is None:
        print('No solution found :(')
    else:
        print('Found solution:')
        k.display(sol)
    
    print('Time:', end-start, 'seconds')

    print('\n----------\n')


