#!/usr/bin/env python
import ply.yacc as yacc
from tokens import tokens

precedence = (
    ('left', 'EQL'),
    ('left', 'IFF'),
    ('left', 'IF', 'FI'),
    ('left', 'OR'),
    ('left', 'AND'),
    ('right', 'NOT'),
    ('right', 'EXISTS'),
)

def p_exists(p):
    '''expr : EXISTS atoms LPAR expr RPAR  %prec EXISTS
    '''
    tree = p[4]
    for atom in p[2]:
        tree = [p[1], atom, tree]
    p[0] = tree

def p_atoms(p):
    '''atoms : ATOM atoms
             | ATOM
    '''
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = [p[1]] + p[2]

def p_expr_paren(p):
    '''expr : LPAR expr RPAR'''
    p[0] = p[2]

def p_expr_unary(p):
    '''expr : NOT expr            %prec NOT'''
    p[0] = [p[1], p[2]]

def p_expr_binop(p):
    '''expr : expr EQL expr       %prec EQL
            | expr IFF expr       %prec IFF
            | expr FI expr        %prec FI
            | expr IF expr        %prec IF
            | expr OR expr        %prec OR
            | expr AND expr       %prec AND
            '''
    p[0] = [p[2], p[1], p[3]]

def p_expr_literal(p):
    '''expr : literal'''
    p[0] = p[1]

def p_literal(p):
    '''literal : FALSE
               | TRUE
               | ATOM'''
    p[0] = p[1]

def p_error(p):
    import sys
    if p is None:
        sys.stdout.write("Unexpected end of file.\n")
    else:
        sys.stdout.write("Syntax error at '%s' on line %d.\n" % (p.value, p.lineno))
    sys.exit(1)

def parse(string):
    parser = yacc.yacc()
    return parser.parse(string)
