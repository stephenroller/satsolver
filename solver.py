#!/usr/bin/env python
from parser import parse

def and_(arg1, arg2):
    if isinstance(arg1, bool) and arg1:
        return arg2
    elif isinstance(arg1, bool) and not arg1:
        return False
    elif isinstance(arg2, bool) and arg2:
        return arg1
    elif isinstance(arg2, bool) and not arg2:
        return False

def or_(arg1, arg2):
    if isinstance(arg1, bool) and arg1:
        return True
    elif isinstance(arg1, bool) and not arg1:
        return arg2
    elif isinstance(arg2, bool) and arg2:
        return True
    elif isinstance(arg2, bool) and not arg2:
        return arg1

def if_(arg1, arg2):
    if isinstance(arg1, bool) and not arg1:
        return True
    elif isinstance(arg2, bool):
        return arg2

def fi_(arg1, arg2):
    return if_(arg2, arg1)

def not_(arg):
    if isinstance(arg, bool):
        return not arg

def iff_(arg1, arg2):
    if isinstance(arg1, bool) and isinstance(arg2, bool):
        return arg1 == arg2

def equiv_(arg1, arg2):
    F = [iff_, arg1, [not_, arg2]]
    if satisfiable(F):
        return False
    else:
        return True

def exists_(variable, expr):
    # represents the QBF style form of the existential operator.
    true_bound = dict([(variable, True)])
    false_bound = dict([(variable, False)])
    r = [or_, simplify(expr, false_bound), simplify(expr, true_bound)]
    return r

def lessthan_(leftvars, rightvars):
    assert len(leftvars) == len(rightvars)
    return [and_, lessthaneq_(leftvars, rightvars), 
                  [not_, lessthaneq_(rightvars, leftvars)]]

def lessthaneq_(leftvars, rightvars):
    assert len(leftvars) == len(rightvars)
    
    tree = True
    for l, r in zip(leftvars, rightvars):
        tree = [and_, tree, [if_, l, r]]
    
    return tree

def greaterthan_(leftvars, rightvars):
    assert len(leftvars) == len(rightvars)
    return [and_, greaterthaneq_(leftvars, rightvars),
                  [not_, greaterthaneq_(rightvars, leftvars)]]

def greaterthaneq_(leftvars, rightvars):
    assert len(leftvars) == len(rightvars)
    
    tree = True
    for l, r in zip(leftvars, rightvars):
        tree = [and_, tree, [if_, r, l]]
    
    return tree

def ident_(*args):
    return args

op_functions = {
    '!': not_,
    '->': if_,
    '<-': fi_,
    '<->': iff_,
    '&': and_,
    '|': or_,
    '<=>': equiv_,
    '3': exists_,
    '<': lessthan_,
    '>': greaterthan_,
    '<=': lessthaneq_,
    '>=': greaterthaneq_,
    'PASS': ident_,
}

# macros are functions that are better defined as a syntactical
# transformation, rather than a function.
macros = [
    ident_,
    lessthan_,
    greaterthan_,
    lessthaneq_,
    greaterthaneq_,
    exists_,
]

def prefix_form(L):
    if isinstance(L, list) and len(L) >= 2:
        operator = op_functions[L[0]]
        if operator in macros:
            return operator(*map(prefix_form, L[1:]))
        else:
            return [operator] + map(prefix_form, L[1:])
    elif isinstance(L, list) and len(L) == 1:
        return prefix_form(L[0])
    else:
        return L

def yield_unbounds(F):
    all_unbounds = []
    if isinstance(F, list):
        for arg in F[1:]:
            for unbound in yield_unbounds(arg):
                if unbound not in all_unbounds:
                    all_unbounds.append(unbound)
                    yield unbound
    elif isinstance(F, str):
        all_unbounds.append(F)
        yield F

def next_unbound(F):
    for unbound in yield_unbounds(F):
        return unbound
    raise StopIteration

def simplify(F, bindings=dict()):
    if isinstance(F, list):
        fn = F[0]
        args = [simplify(a, bindings) for a in F[1:]]
        r = fn(*args)
        if r is not None:
            return r
        else:
            return [fn] + args
    elif isinstance(F, str) and F in bindings:
        return bindings[F]
    else:
        return F

def dpll(F, bindings=dict()):
    F = simplify(F, bindings)
    
    if F is True:
        yield bindings or F
        return
    elif F is False:
        return
    
    L = next_unbound(F)
    
    bindings1 = bindings.copy()
    bindings1[L] = True
    for sat in dpll(F, bindings1):
        yield sat

    bindings2 = bindings.copy()
    bindings2[L] = False
    for sat in dpll(F, bindings2):
        yield sat

def satisfiable(F):
    for sat in dpll(F):
        return sat
    return False

def solutions(exprstr):
    expression = prefix_form(parse(exprstr))
    return dpll(expression)
    
if __name__ == '__main__':
    import sys
    
    example = len(sys.argv) > 1 and sys.argv[1] or "a | b"
    example = example.replace("\n", " ")
    while True:
        r = example.replace("  ", " ")
        if r == example:
            break
        example = r
    
    print "=?", example
    satisfied = False
    for solution in solutions(example):
        print "=>", solution
        satisfied = True
    if not satisfied:
        print "unsatisfiable."
    print "done."
