#!/usr/bin/env python

from solver import solutions

"""
A small example showing how a SAT solver can be used to do a k-coloring
of a graph.
"""

# two colors
colors = ['red', 'blue']
k = len(colors)

# example graph
#
#     a ---- b ---- c
#
V = ['a', 'b', 'c']
E = [('a', 'b'), ('b', 'c')]

# every vertex has a color
F1 = " & ".join("(" + " | ".join("p_%s_%d" % (v, i) 
                for i in range(0, k)) + ")" for v in V)

# every vertex has only one color
F2 = " & ".join("!(p_%s_%d & p_%s_%d)" % (v, i, v, j) 
                for i in range(k)
                for j in range(i+1, k)
                for v in V)

# no adjacent vertices have the same color
F3 = " & ".join("!(p_%s_%d & p_%s_%d)" % (v, i, w, i)
                for i in range(k)
                for (v, w) in E)

# conjunction of these three rules
F = "%s & %s & %s" % (F1, F2, F3)

for solution in solutions(F):
    coloring = {}
    for (k, v) in solution.iteritems():
        if v:
            (p, v, c) = k.split("_")
            c = int(c)
            coloring[v] = colors[c]
    print coloring

print "done."