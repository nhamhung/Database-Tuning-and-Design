###########################################################################
## answers.py - Code template for Project Functional Dependencies
###########################################################################

## If you need to import library put it below

from itertools import chain, combinations, permutations, product

## Change the function below with your student number.
def student_number():
    return 'A0187652U'

## Q1a. Determine the closure of a given set of attribute S the schema R and functional dependency F
def closure(R, F, S):
    """
    Compute closure of an att_set based on the fd_set
    """
    closed = set(S)
    unused = F.copy()
    changed = True
    while changed:
        changed = False
        for fd in unused.copy():
            # lhs of current fd is a subset of att_set closed
            if set(fd[0]).issubset(closed):
                closed.update(set(fd[1]))
                # early termination
                if len(closed) == len(R):
                    break
                unused.remove(fd)
                changed = True
            
    return list(closed)

## Q1b. Determine all attribute closures excluding superkeys that are not candidate keys given the schema R and functional dependency F
def all_closures(R, F): 
    """
    Compute closures of all subsets of the fd_set excluding super keys that are not candidate keys
    """
    all_subsets = get_all_subsets(R)
    result = []

    all_subsets_copy = all_subsets.copy()

    while len(all_subsets_copy) > 0:
        attr_set = all_subsets_copy.pop(0)
        attr_set_closure = closure(R, F, attr_set)
        if len(attr_set_closure) == 0:
            continue
        if set(attr_set_closure) == set(R):
            all_subsets_copy = [attr_set_copy for attr_set_copy in all_subsets_copy if not set(attr_set_copy).issuperset(set(attr_set))]
    
        result.append([list(attr_set), attr_set_closure])

    return result
    
## Q2a. Return a minimal cover of the functional dependencies of a given schema R and functional dependencies F.
def min_cover(R, FD): 
    """
    Compute a minimal cover of the given fd_set according to the following steps:
    1. Minimize rhs of all FDs
    2. Minimize lhs of all FDs
    3. Remove redundant FDs
    """
    result = minimize_rhs_all_fds(FD)
    result = minimize_lhs_all_fds(R, result)
    minimal_cover = remove_redundant_fds(R, result)
    return minimal_cover

## Q2b. Return all minimal covers reachable from the functional dependencies of a given schema R and functional dependencies F.
def min_covers(R, FD):
    """
    Compute all minimal covers reachable from the given FD according to the following steps:
    1. Minimize rhs of all FDs
    2. Get all possible combinations of left-minimized FDs
    3. For each combination which is a left-minimized FD, get unique minimal covers from all of its permutations
    """
    # minimize rhs
    rminimized_fd_set = minimize_rhs_all_fds(FD)
    all_lminimized = {}
    # compute all possible minimized subsets of each lhs
    for lhs, rhs in rminimized_fd_set:
        all_lminimized[(tuple(lhs), tuple(rhs))] = set()

        min_len = len(lhs) 
        for lhs_subset in chain.from_iterable(combinations(lhs, r) for r in range(0, len(lhs) + 1)):
            if implies(R, list(lhs_subset), rhs, rminimized_fd_set) and len(lhs_subset) <= min_len:
                min_len = len(lhs_subset)
                all_lminimized[(tuple(lhs), tuple(rhs))].add(tuple(sorted(list(lhs_subset))))
    
    x = [list(lhs) for lhs in list(all_lminimized.values())]
    all_rhs = [rhs for _, rhs in rminimized_fd_set]
    # use cartesian product to get all possible left-minimized fd_set
    cartesian_product = [[list(x) for x in group] for group in list(product(*x))]
    all_lminimized_fd_set = [list(zip(product, all_rhs)) for product in cartesian_product]
    all_lminimized_fd_set = [[list(x) for x in group] for group in all_lminimized_fd_set]

    # for each left-minimized fd_set, get all unique minimal covers for different permutations
    all_minimal_covers = set()

    for lminimized_fd_set in all_lminimized_fd_set:
        for permutation in permutations(lminimized_fd_set, len(lminimized_fd_set)):
            minimum_cover = remove_redundant_fds(R, list(permutation))
            hashable_minimum_cover = get_hashable_fd_set(minimum_cover)
            all_minimal_covers.add(hashable_minimum_cover)

    return [[[list(lhs), list(rhs)] for lhs, rhs in min_cover] for min_cover in all_minimal_covers]

## Q2c. Return all minimal covers of a given schema R and functional dependencies F.
def all_min_covers(R, FD):
    """
    Get all minimal covers for a given FD according to the following steps:
    1. Compute FD+ from FD
    2. Remove trivial fd from FD+
    3. Apply min_covers on FD+ to obtain all minimal covers
    """
    all_minimal_covers = set()
    # compute fd_plus which is the set closure of fd_set
    fd_plus = set_closure(R, FD)
    fd_plus = [fd for fd in fd_plus if not set(fd[0]).issuperset(set(fd[1]))]
    # apply min_covers on fd_plus to get all minimal covers
    minimal_covers = min_covers(R, fd_plus)

    for minimum_cover in minimal_covers:
        all_minimal_covers.add(get_hashable_fd_set(minimum_cover))

    return [[[list(lhs), list(rhs)] for lhs, rhs in min_cover] for min_cover in all_minimal_covers]

## You can add additional functions below

def get_all_subsets(lst):
    return list(chain.from_iterable(combinations(lst, r) for r in range(0, len(lst) + 1)))

def implies(schema, lhs, rhs, fd_set):
    """
    Check whether the current fd_set implies the fd [lhs, rhs]
    """
    return set(closure(schema, fd_set, lhs)).issuperset(set(rhs))

def set_closure(schema, fd_set):
    """
    Get the set closure of a given fd_set
    """
    fd_plus = []
    L = get_all_subsets(schema)
    
    for attr_set in L:
        attr_set_closure = closure(schema, fd_set, attr_set)
        for attr in attr_set_closure:
            fd_plus.append([list(attr_set), list(attr)])
        
    return fd_plus

def get_hashable_fd_set(fd_set):
    """
    Get a hashable version of the fd_set to remove duplicates
    """
    return tuple(sorted(list(((tuple(lhs), tuple(rhs)) for lhs, rhs in fd_set))))

def minimize_lhs_current_fd(schema, lhs, rhs, fd_set):
    """
    Minimize the lhs of this fd [lhs, rhs] by removing each attribute of lhs
    """
    lhs_copy = lhs.copy()
    for attr in lhs:
        lhs_copy.remove(attr)
        if not implies(schema, lhs_copy, rhs, fd_set):
            lhs_copy.append(attr)
    return lhs_copy

def minimize_rhs_all_fds(fd_set):
    """
    Minimize the rhs to a single attribute for every fd in the fd_set
    """
    fd_set_rminimized = []

    for lhs, rhs in fd_set:
        for attr in rhs:
            if [lhs, attr] not in fd_set_rminimized:
                fd_set_rminimized.append([lhs, [attr]])
    
    return fd_set_rminimized

def minimize_lhs_all_fds(schema, fd_set):
    """
    Minimize the lhs for every fd in the fd_set
    """
    fd_set_lminimized = []
    for lhs, rhs in fd_set:
        lhs_minimized = minimize_lhs_current_fd(schema, lhs, rhs, fd_set)
        if lhs_minimized != lhs:
            fd_set_lminimized.append([lhs_minimized, rhs])
        else:
            fd_set_lminimized.append([lhs, rhs])
    return fd_set_lminimized

def remove_redundant_fds(schema, fd_set):
    """
    Check whether without each FD fd, the fd_set can still imply fd
    """
    fd_set_copy = fd_set.copy()
    for fd in fd_set:
        fd_set_copy.remove(fd)
        if not implies(schema, fd[0], fd[1], fd_set_copy):
            fd_set_copy.append(fd)
    
    return fd_set_copy

## Main functions
def main():
    ### Test case from the project
    R = ['A', 'B', 'C', 'D']
    FD = [[['A', 'B'], ['C']], [['C'], ['D']]]

    print(closure(R, FD, ['A']))
    print(closure(R, FD, ['A', 'B']))
    print(all_closures(R, FD))

    R = ['A', 'B', 'C', 'D', 'E', 'F']
    FD = [[['A'], ['B', 'C']], [['B'], ['C','D']], [['D'], ['B']], [['A','B','E'], ['F']]]
    print(min_cover(R, FD)) 

    R = ['A', 'B', 'C']
    FD = [[['A'], ['B']], [['B'], ['C']], [['C'], ['A']]] 
    print(min_covers(R, FD))
    print(all_min_covers(R, FD)) 

    ### Add your own additional test cases if necessary


if __name__ == '__main__':
    main()