# a collection of helpful debug functions

def treediff(tree1, tree2):
    if isinstance(tree1, list) and isinstance(tree2, list) and len(tree1) == len(tree2):
        for branch1, branch2 in zip(tree1, tree2):
            treediff(branch1, branch2)
    elif tree1 == tree2 or not isinstance(tree1, list) or not isinstance(tree2, list):
        pass
    else:
        import pprint
        print "Tree 1:"
        pprint.pprint(tree1)
        print
        print "Tree 2:"
        pprint.pprint(tree2)
        print
        print "-" * 60
        print

