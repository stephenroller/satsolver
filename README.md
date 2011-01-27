# Simple SAT Solver

This is a simple SAT solver implemented in Python.

## Example Usage:

    $ python solver.py 'a'
    =? a
    => {'a': True}
    done.
    
    $ python solver.py 'a | b'
    =? a | b
    => {'a': True}
    => {'a': False, 'b': True}
    done.
    
    sr ~/Wo/satsolver $ python solver.py 'a & !a'
    =? a & !a
    unsatisfiable.
    done.

## Base Connectors

  * false (0)
  * true (1)
  * conjunction (&)
  * disjunction (|)
  * not (!)
  * implication (->)
  * reverse implication (<-)
  * biconditional (<->)
  * equivalence (<=>)

Not that an equivalence formula, a <=> b, is true iff a <-> b is a tautology.
