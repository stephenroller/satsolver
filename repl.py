#!/usr/bin/env python
import sys
from solver import solutions as solutions_finder
from parser import SATSyntaxError, SATEndOfFileError

def nice_display(variables):
    return "  ".join( (v and " %s" or "!%s") % k 
                      for k,v in variables.iteritems() )

if __name__ == '__main__':
    while True:
        try:
            F = raw_input('> ').strip()
            if not F:
                continue
            
            while True:
                # keep getting input until we have a full expression
                try:
                    solutions = solutions_finder(F)
                    break
                except SATEndOfFileError:
                    # not done getting the full expression
                    F += " " + raw_input('... ').strip()
                    continue
                except SATSyntaxError, se:
                    # syntax error! report it
                    print "! " + F 
                    sys.stdout.write('-' * (se.charnum + 2) + '^\n')
                    sys.stdout.write(se.mesg + '\n')
                    raise
            
            satisfied = False
            for solution in solutions:
                print "= ", nice_display(solution)
                satisfied = True
            if not satisfied:
                print "unsatisfiable."
        except SATSyntaxError, s:
            continue
        except (KeyboardInterrupt,EOFError):
            print
            break
    
