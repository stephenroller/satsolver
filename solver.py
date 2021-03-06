#!/usr/bin/env python
from parser import parse, SATSyntaxError

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
    if isinstance(arg1, bool) and arg1:
        return arg2
    elif isinstance(arg1, bool) and not arg1:
        return True
    elif isinstance(arg2, bool) and arg2:
        return True

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
    r = [or_, simplify(expr, false_bound, False), simplify(expr, true_bound, False)]
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

def circ_(vars1, expr):
    '''
    The Circumscription operator, which finds minimal models. (see sm_)
    '''
    vars2 = [v + '_' for v in vars1]
    
    rename_bindings = dict(zip(vars1, vars2))
    replaced = simplify(expr, rename_bindings, infer=False)
    
    tree = [and_, lessthan_(vars2, vars1), replaced]
    for var_ in vars2:
        tree = exists_(var_, tree)
    tree = [and_, expr, [not_, tree]]
    
    return tree


def f_diamond(expr, replacements):
    '''
    The F-diamond operator described in 
    http://www.cs.utexas.edu/users/vl/papers/dpsm.pdf
    '''
    if isinstance(expr, list):
        fn = expr[0]
        args = expr[1:]
        if fn == not_:
            return expr
        else:
            return [fn] + [f_diamond(arg, replacements) for arg in args]
    elif isinstance(expr, str) and expr in replacements:
        return replacements[expr]
    else:
        return expr

def f_star(expr, replacements):
    if isinstance(expr, list):
        fn = expr[0]
        args = expr[1:]
        if fn == not_:
            return f_star([if_, args[0], False], replacements)
        elif fn == if_:
            return [and_, [if_, f_star(args[0], replacements), 
                                f_star(args[1], replacements)],
                          expr]
        else:
            return [fn, f_star(args[0], replacements), f_star(args[1], replacements)]
    elif isinstance(expr, str) and expr in replacements:
        return replacements[expr]
    else:
        return expr


def sm_(vars1, expr, f_operator=f_star):
    vars2 = [v + '_' for v in vars1]
    
    rename_bindings = dict(zip(vars1, vars2))
    replaced = f_operator(expr, rename_bindings)
    
    tree = [and_, lessthan_(vars2, vars1), replaced]
    for var_ in vars2:
        tree = exists_(var_, tree)
    tree = [and_, expr, [not_, tree]]
    
    return tree

def smdl_(vars1, expr):
    return sm_(vars1, expr, f_operator=f_diamond)

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
    'CIRC': circ_,
    'SM': sm_,
    'SMDL': smdl_,
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
    circ_,
    sm_,
]

def parse2ast(L):
    if isinstance(L, list) and len(L) >= 2:
        operator = op_functions[L[0]]
        if operator in macros:
            return operator(*map(parse2ast, L[1:]))
        else:
            return [operator] + map(parse2ast, L[1:])
    elif isinstance(L, list) and len(L) == 1:
        return parse2ast(L[0])
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

def simplify(F, bindings=dict(), infer=True):
    '''
    Simplifies a formula by replacing variables with their bound values.
    
    If infer is True, then it will attempt to simplify the formula by
    simple inference rules, such as T -> p => p.
    
    Otherwise, simplify will only dumbly replace variables.
    '''
    if isinstance(F, list):
        fn = F[0]
        args = [simplify(a, bindings, infer) for a in F[1:]]
        r = fn(*args)
        if r is not None and infer:
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
    expression = parse2ast(parse(exprstr))
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
    try:
        for solution in solutions(example):
            print "=>", solution
            satisfied = True
        if not satisfied:
            print "unsatisfiable."
    except SATSyntaxError, se:
        if se.charnum >= 0:
            print "-" * (se.charnum + 3) + '^'
        print se.mesg
        sys.exit(1)
    print "done."
