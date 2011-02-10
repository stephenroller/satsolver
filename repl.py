#!/usr/bin/env python
import sys
from solver import solutions as solutions_finder
from parser import SATSyntaxError, SATEndOfFileError

if __name__ == '__main__':
    while True:
        try:
            F = raw_input('> ').strip()
            if not F:
                continue
            
            # keep getting input until we have a full expression
            while True:
                try:
                    solutions = solutions_finder(F)
                    print "? " + F
                    break
                except SATEndOfFileError:
                    F += " " + raw_input('... ').strip()
                    continue
                except SATSyntaxError, se:
                    print "! " + F 
                    sys.stdout.write('-' * (se.charnum + 2) + '^\n')
                    sys.stdout.write(se.mesg + '\n')
                    raise
            
            satisfied = False
            for solution in solutions:
                print "=>", solution
                satisfied = True
            if not satisfied:
                print "unsatisfiable."
        except SATSyntaxError, s:
            continue
        except (KeyboardInterrupt,EOFError):
            print
            break
    
