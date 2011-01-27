# Simple SAT Solver

A simple SAT solver implemented in Python.

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
    
    $ python solver.py 'a & !a'
    =? a & !a
    unsatisfiable.
    done.
    
    $ python solver.py '(p -> q) <=> (!p | q)'
    =? (p -> q) <=> (!p | q)
    => True
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

## Implementation

The implementation of this SAT solver is a very simplistic implementation of
the [DPLL algorithm](http://en.wikipedia.org/wiki/DPLL_algorithm).

## Other Uses

twocolor.py shows how predicate logic can be simply used to describe a 
two-coloring of a graph.