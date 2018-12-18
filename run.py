import kenken, kenken_problems, csp
import sys

# prior to writing this, i thought good code did not exist...
# now i'm certain
if __name__ == '__main__':
    try:
        pname = sys.argv[1]
    except:
        pname = 'six'
    finally:
        try:
            puzzle = getattr(kenken_problems, pname)
        except:
            puzzle = getattr(kenken_problems, 'six')
    
    try:
        algo = sys.argv[2].lower()
    except:
        algo = 'fc_mrv'

    # setup
    k = kenken.Kenken(puzzle)

    # AC3 to reduce domains
    csp.AC3(k)

    # solve and display
    if algo == 'bt':
        sol = csp.backtracking_search(k)
    elif algo == 'bt_mrv':
        sol = csp.backtracking_search(k, csp.mrv)
    elif algo == 'fc':
        sol = csp.backtracking_search(k, inference=csp.forward_checking)
    elif algo == 'fc_mrv':
        sol = csp.backtracking_search(k, csp.mrv, inference=csp.forward_checking)
    elif algo == 'mac':
        sol = csp.backtracking_search(k, inference=csp.mac)
    elif algo == 'minconflicts':
        sol = csp.min_conflicts(k)

    if sol is None:
        print('No solution found :(')
    else:
        k.display(sol)

