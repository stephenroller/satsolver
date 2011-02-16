# Simple SAT Solver

A simple SAT solver implemented in Python (with some non-SAT abilities).

## Example Usage:

    $ python repl.py 'a'
    > p
    =   p

    > p | q
    =   p
    =   q, !p

    > p & !p
    unsatisfiable.

    > (p -> q) <=> (!p | q)
    =  True
 
## Connectors

  * false (0)
  * true (1)
  * conjunction (&)
  * disjunction (|)
  * not (!)
  * implication (->)
  * reverse implication (<-)
  * biconditional (<->)

A bicontional formula, a <-> b, is rewritten as (a -> b) & (b -> a).

### Special connectors

These operators have no place in any SAT solver, but here they are anyway:

  * equivalence (A <=> B) - Returns true if and only if A <-> B is a tautology.
  * CIRC p1, p2, ... [ F ] - The [circumscription][circ] operator, which finds
    minimal models.
  * SM p1, p2, ... [ F ] - The [stable models][sm] operator, which finds
    stable models.
  * (p1, p2, ...) <= (q1, q2, ...) - Shorthand for (p1 -> q1) & (p2 -> q2) & ... 
  * (p1, p2, ...) < (q1, q2, ...) - Shorthand for 
    ((p1, ...) <= (q1, ...)) & !((q1, ...) <= (p1, ...))
  * 3 z ( F ) - The existential quantifier as in [quantified boolean formulas][qbf]

[circ]: http://z.cs.utexas.edu/users/ai-lab/pub-view.php?PubID=970
[sm]: http://z.cs.utexas.edu/users/ai-lab/pub-view.php?PubID=126919 
[qbf]: http://en.wikipedia.org/wiki/True_quantified_Boolean_formula

## Implementation

The implementation of this SAT solver is a very naïve implementation of
the [DPLL algorithm](http://en.wikipedia.org/wiki/DPLL_algorithm).

The <=>, CIRC and SM operators are written by rewriting the equations using
their definitions.

### Inefficiency

This program is horribly inefficient. Do not use it.

## Other Examples

twocolor.py shows how predicate logic can be simply used to describe a 
two-coloring of a graph.