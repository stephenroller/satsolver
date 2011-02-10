from solver import *

if __name__ == '__main__':
    import sys
    
    # while True:
    #     sys.stdout.write("> ")
    #     
    #     print "=?", example
    
    while True:
        try:
            F = raw_input('> ')
            satisfied = False
            for solution in solutions(F):
                print "=>", solution
                satisfied = True
            if not satisfied:
                print "unsatisfiable."
        except KeyboardInterrupt:
            print
            break
    