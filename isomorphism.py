# -*- coding: utf-8 -*-
"""
Created on Sat May 14 21:13:47 2022

@author: rober
"""

import itertools

# Returns whether f is an isomorphism from g1 to g2.
def is_isomorphism(f, g1, g2):
    # Check that g1 and g2 are of the same order
    if g1.order() != g2.order():
        return False
    
    # Check that f is surjective
    image = [f(a) for a in g1]
    for a in g2:
        if not a in image:
            return False
    
    # Check that f respects the group operation
    for a, b in itertools.product(g1.elements, repeat=2):
        with g1.mul():
            p1 = f(a*b)
        with g2.mul():
            p2 = f(a)*f(b)
        if p1 != p2:
            return False
    
    return True

class Function:
    def __init__(self, f, domain, codomain):
        self.f = dict()
        
        for x in domain:
            y = f[x] if isinstance(f, dict) else f(x)
            if not y in codomain:
                raise ValueError('f({}) = {} not in codomain'.format(x, y))
            self.f[x] = y
    
    def __apply__(self, x):
        return self.f[x]

def all_isomorphisms_helper(g1, g2, f):
    pass

# Return a list of all isomorphisms from g1 to g2.
def all_isomorphisms(g1, g2):
    f = {g1.identity: g2.identity}
    
    # For now, do it the dumb way
    g1_rest = list(g1)
    g1_rest.remove(g1.identity)
    g2_rest = list(g2)
    g2_rest.remove(g2.identity)
    
    # Go through all bijections from g1 to g2 that map identity to identity
    # and keep only the isomorphisms
    isos = list()
    for perm in itertools.permutations(g2_rest):
        iso = dict(f)
        for x, y in zip(g1_rest, perm):
            iso[x] = y
        
        if is_isomorphism(iso, g1, g2):
            isos.append(Function(iso))
    
    return isos