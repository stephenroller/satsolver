#!/usr/bin/env python
import sys
from solver import *

if __name__ == '__main__':
    while True:
        try:
            F = raw_input('> ')
            satisfied = False
            for solution in solutions(F):
                print "=>", solution
                satisfied = True
            if not satisfied:
                print "unsatisfiable."
        except (KeyboardInterrupt,EOFError):
            print
            break
    
